import os
from flask import Flask, request, jsonify
import io
from PIL import Image
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from google.cloud import vision
from google.api_core import exceptions
from tenacity import retry, wait_exponential, stop_after_attempt
import random
import json
import os
import logging
import random
from pathlib import Path
from flask_cors import CORS
from flask import jsonify
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8000"}})


# Configuración de credenciales para Google Cloud Vision
# Asegúrate de que el archivo google-credentials.json esté en C:\REGLAS\
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google-credentials.json'
vision_client = vision.ImageAnnotatorClient()

# Carga de modelos preentrenados
# Modelos deben estar en C:\REGLAS\ junto con las credenciales
# Cargar los modelos
try:
    fashion_model = load_model('fashion_model.h5')
    calzado_model = load_model('modamind_calzado_modelo.h5')
    emotion_model = load_model('face_emotion_model_reduced.h5')
    print("Modelos cargados exitosamente.")
except Exception as e:
    print(f"Error al cargar los modelos: {e}")
    raise Exception("Por favor, verifica que los archivos .h5 estén  y que TensorFlow esté correctamente instalado.")
try:
    reglas_path = Path("reglas.json")
    if reglas_path.exists():
        with open(reglas_path, encoding="utf-8") as f:
            REGLAS_MODA = json.load(f)
    else:
        logging.error("reglas.json no encontrado. Usando reglas vacías.")
        REGLAS_MODA = {}
except (FileNotFoundError, json.JSONDecodeError) as e:
    logging.error(f"Error al cargar reglas.json: {e}")
    REGLAS_MODA = {}

try:
    recomendaciones_path = Path("recomendaciones.json")
    if not recomendaciones_path.exists():
        raise FileNotFoundError(f"No se encontró {recomendaciones_path}")
    with open(recomendaciones_path, encoding="utf-8") as f:
        RECOMENDACIONES_AVANZADAS = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logging.error(f"Error al cargar recomendaciones.json: {e}")
    RECOMENDACIONES_AVANZADAS = {}

with open("armario_digital.json", encoding="utf-8") as f:
    ARMARIOS = json.load(f)

try:
    armario_path = Path("armario_digital.json")
    if armario_path.exists():
        with open(armario_path, encoding="utf-8") as f:
            ARMARIOS = json.load(f)
    else:
        logging.warning("armario_digital.json no encontrado. Usando armario vacío.")
        ARMARIOS = {}
except (FileNotFoundError, json.JSONDecodeError) as e:
    logging.error(f"Error al cargar armario_digital.json: {e}")
    ARMARIOS = {}    

LUGARES = {
    "playa": {"nombre": "Playa", "eventos": ["boda", "paseo", "reunion_social", "relajacion"]},
    "montana_bosque": {"nombre": "Montaña/Bosque", "eventos": ["senderismo", "camping", "comida_aire_libre", "exploracion"]},
    "campo": {"nombre": "Campo", "eventos": ["festival", "paseo", "reunion_familiar", "excursion"]},
    "paseo_casual": {"nombre": "Paseo Casual (Urbano)", "eventos": ["compras", "paseo", "reunion_amigos", "visita_cultural"]},
    "espacio_publico": {"nombre": "Espacio Público", "eventos": ["mercado", "concierto", "evento_deportivo", "reunion_comunitaria"]},
    "salida_nocturna": {"nombre": "Salida Nocturna", "eventos": ["cena_trabajo", "fiesta", "cita_romantica", "evento_corporativo"]},
    "espacio_laboral": {"nombre": "Espacio Laboral", "eventos": ["reunion", "presentacion", "entrevista", "trabajo_diario"]},
    "restaurante_bar": {"nombre": "Restaurante/Bar", "eventos": ["cena", "cita", "celebracion", "reunion_informal"]},
    "espacio_diario": {"nombre": "Espacio Diario", "eventos": ["clases_universitarias", "ir_mercado", "hacer_quehaceres", "estar_casa"]},
    "gimnasio_parque": {"nombre": "Gimnasio/Parque Deportivo", "eventos": ["ejercicio", "clase_fitness", "competencia", "caminata"]},
    "iglesia": {"nombre": "Iglesia", "eventos": ["boda", "confirmacion", "misa", "evento_religioso", "velorio"]}
}
EVENTOS = {
  "boda": "Ceremonias nupciales",
  "paseo": "Caminatas o paseos",
  "reunion_social": "Encuentros informales",
  "relajacion": "Descanso o lectura",
  "senderismo": "Excursiones",
  "camping": "Pernoctaciones",
  "comida_aire_libre": "Comidas",
  "exploracion": "Aventuras",
  "festival": "Eventos culturales",
  "reunion_familiar": "Celebraciones",
  "excursion": "Salidas",
  "compras": "Visitas a tiendas",
  "reunion_amigos": "Encuentros informales",
  "visita_cultural": "Exploración de museos",
  "mercado": "Compra en mercados",
  "concierto": "Actuaciones musicales",
  "evento_deportivo": "Competencias",
  "reunion_comunitaria": "Encuentros",
  "cena_trabajo": "Reuniones profesionales",
  "fiesta": "Celebraciones",
  "cita_romantica": "Salidas íntimas",
  "evento_corporativo": "Galas",
  "reunion": "Encuentros de trabajo",
  "presentacion": "Exposiciones",
  "entrevista": "Reuniones formales",
  "trabajo_diario": "Actividades rutinarias",
  "cena": "Comidas",
  "cita": "Encuentros románticos",
  "celebracion": "Cumpleaños",
  "reunion_informal": "Encuentros casuales",
  "clases_universitarias": "Actividades educativas",
  "ir_mercado": "Compras diarias",
  "hacer_quehaceres": "Tareas domésticas",
  "estar_casa": "Relajación",
  "ejercicio": "Entrenamiento",
  "clase_fitness": "Sesiones guiadas",
  "competencia": "Torneos",
  "caminata": "Paseos",
  "confirmacion": "Ritos religiosos",
  "misa": "Servicios religiosos",
  "evento_religioso": "Celebraciones",
  "velorio": "Servicios fúnebres"
}

GENEROS = ["hombres", "mujeres"]
EMOCIONES = ["feliz", "triste", "neutro"]
TIPOS_CUERPO = {
    "hombres": ["sin_tipo", "triangulo_invertido", "rectangulo", "ovalado", "trapezoide", "triangulo"],
    "mujeres": ["sin_tipo", "reloj_arena", "triangulo_pera", "triangulo_invertido", "rectangulo", "ovalado_manzana"]
}
ARMARIO_DIGITAL = ["con_armario", "sin_armario"] 

ARMARIOS = {
    "usuario1": {
        "mujeres": {
            "parte_superior": {
                "camisetas_blusas": ["camiseta_casual", "blusa", "top", "crop_top", "vividi"],
                "camisas": ["camisa_formal", "camisa_casual", "camisa_vestir"],
                "sueteres_buzos": ["buzo_con_capucha", "buzo_sin_capucha", "sueter_ligero"],
                "abrigos_chaquetas": ["chaqueta_gruesa", "saco", "abrigo", "parka"],
                "vestidos_enterizos": ["vestido_casual", "vestido_noche", "vestido_formal", "vestido_veraniego", "jumpsuit", "mono", "overalls"]
            },
            "parte_inferior": {
                "pantalones": ["jeans", "leggings", "pantalon_formal", "pantalon_casual", "pantalon_deportivo"],
                "faldas": ["falda_corta", "falda_midi", "falda_larga", "falda_casual", "falda_vestir"],
                "shorts": ["short_casual", "short_deportivo"]
            },
            "calzado": {
                "deportivo": ["zapatillas", "tenis"],
                "casual": ["zapatos_casual", "flats"],
                "formal": ["tacones", "zapatos_vestir"],
                "botas_sandalias": ["botas", "botines", "sandalias_casual", "sandalias_formal"]
            }
        },
        "hombres": {
            "parte_superior": {
                "camisetas": ["camiseta_manga_corta", "camiseta_manga_larga", "camiseta_sin_mangas", "vividi", "camiseta_deportiva"],
                "camisas": ["camisa_formal", "camisa_casual", "camisa_vestir"],
                "sueteres_buzos": ["buzo_con_capucha", "buzo_sin_capucha", "sueter_ligero"],
                "abrigos_chaquetas": ["chaqueta_gruesa", "saco", "abrigo", "parka"]
            },
            "parte_inferior": {
                "pantalones": ["jeans", "pantalon_formal", "pantalon_casual", "pantalon_deportivo"],
                "shorts": ["short_casual", "short_deportivo", "bermuda"]
            },
            "calzado": {
                "deportivo": ["zapatillas", "tenis"],
                "casual": ["zapatos_casual", "mocasines"],
                "formal": ["zapatos_vestir", "oxfords"],
                "botas_sandalias": ["botas_invierno", "sandalias_casual"]
            }
        }
    }
}

def traducir_etiqueta_modelo(etiqueta, genero="mujeres", contexto_formalidad=None):
    etiqueta = etiqueta.lower()
    traducciones = {
        "blazer": "chaqueta_formal",
        "blouse": "blusa" if genero == "mujeres" else "camisa_formal",
        "bodysuit": "body",
        "button_down": "camisa_vestir" if contexto_formalidad in ["formal", "semi_formal"] else "camisa",
        "cardigan": "cardigan",
        "hoodie": "buzo",
        "jacket": "chaqueta" if contexto_formalidad == "casual" else "chaqueta_gruesa",
        "sweater": "sueter_ligero",
        "sweatshirt": "buzo",
        "tank": "camiseta_sin_mangas",
        "tee": "camiseta",
        "tshirt": "camiseta",
        "top": "top",
        "turtleneck": "cuello_alto",
        "kimono": "kimono",
        "coat": "abrigo",
        "trench_coat": "gabardina",
        "cape": "capa",
        "halter": "blusa_sin_hombros",
        "tube": "top_sin_tirantes",
        "vest": "chaleco",

        "pant": "pantalon" if contexto_formalidad == "casual" else "pantalon_formal",
        "pants": "pantalon" if contexto_formalidad == "casual" else "pantalon_formal",
        "jeans": "jeans",
        "joggers": "pantalon_deportivo",
        "leggings": "leggings",
        "overalls": "overol",
        "romper": "enterizo_corto",
        "jumpsuit": "enterizo",
        "shorts": "short",
        "skirt": "falda_midi" if genero == "mujeres" else "bermuda",
        "suit": "traje_formal",
        "dress": "vestido_veraniego" if contexto_formalidad == "casual" else "vestido",

        "boots": "botas",
        "sandals": "sandalias" if contexto_formalidad == "casual" else "sandalias_formal",
        "shoes": "zapatos",
        "slippers": "pantuflas",
        "clogs": "zuecos",
        "sneakers": "zapatillas",
        "heels": "tacones" if genero == "mujeres" else "zapatos_formales",
        "flats": "zapatos_bajos",
        "oxfords": "zapatos_oxford",
        "loafers": "mocasines",
        "espadrilles": "alpargatas",
        "flip_flops": "sandalias_playeras",
        "wedges": "plataformas",
        "mules": "mules",
        "derby": "zapatos_derby",
        "brogues": "zapatos_brogue",
        "slingbacks": "zapatos_con_correa",
        "mary_janes": "merceditas"
    }
    return traducciones.get(etiqueta, etiqueta)

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def detect_clothing(image_content, lugar='espacio_diario', evento='general', genero='mujeres'):
    img_array = preprocess_image(image_content)

    try:
        fashion_prediction = fashion_model.predict(img_array)
        print("fashion_model prediction (raw):", fashion_prediction)
    except Exception as e:
        print(f"Error al predecir con fashion_model: {e}")
        fashion_prediction = np.array([[0]*33]) 

    total_categories = ['blazer', 'blouse', 'bodysuit', 'button_down', 'cardigan', 'hoodie', 'jacket', 'sweater',
                       'sweatshirt', 'tank', 'tee', 'tshirt', 'top', 'turtleneck', 'kimono', 'coat', 'trench_coat',
                       'cape', 'halter', 'tube', 'vest', 'pant', 'pants', 'jeans', 'joggers', 'leggings', 'overalls',
                       'romper', 'jumpsuit', 'shorts', 'skirt', 'suit', 'dress']
    predicted_category_index = np.argmax(fashion_prediction[0])
    predicted_category = total_categories[predicted_category_index] if predicted_category_index < len(total_categories) else "Desconocido"

    formalidad = REGLAS_MODA.get(lugar, {}).get(evento, {}).get("formalidad", "casual")

    upper_clothing_categories = ['blazer', 'blouse', 'bodysuit', 'button_down', 'cardigan', 'hoodie', 'jacket', 'sweater',
                                'sweatshirt', 'tank', 'tee', 'tshirt', 'top', 'turtleneck', 'kimono', 'coat', 'trench_coat',
                                'cape', 'halter', 'tube', 'vest']
    lower_clothing_categories = ['pant', 'pants', 'jeans', 'joggers', 'leggings', 'overalls', 'romper', 'jumpsuit',
                                'shorts', 'skirt', 'suit', 'dress']

    upper_clothing = [traducir_etiqueta_modelo(predicted_category, genero, formalidad)] if predicted_category in upper_clothing_categories else []
    lower_clothing = [traducir_etiqueta_modelo(predicted_category, genero, formalidad)] if predicted_category in lower_clothing_categories else []

    try:
        calzado_prediction = calzado_model.predict(img_array)
        print("calzado_model prediction (raw):", calzado_prediction)
    except Exception as e:
        print(f"Error al predecir con calzado_model: {e}")
        calzado_prediction = np.array([[0]*18])

    footwear_categories = ['boots', 'sandals', 'shoes', 'slippers', 'clogs', 'sneakers', 'heels', 'flats', 'oxfords',
                          'loafers', 'espadrilles', 'flip_flops', 'wedges', 'mules', 'derby', 'brogues', 'slingbacks', 'mary_janes']
    predicted_footwear_index = np.argmax(calzado_prediction[0])
    footwear = [traducir_etiqueta_modelo(footwear_categories[predicted_footwear_index], genero, formalidad)] if predicted_footwear_index < len(footwear_categories) else []

    try:
        emotion_prediction = emotion_model.predict(img_array)
        print("emotion_model prediction (raw):", emotion_prediction)
    except Exception as e:
        print(f"Error al predecir con emotion_model: {e}")
        emotion_prediction = np.array([[0]*3])

    if len(emotion_prediction.shape) > 1 and emotion_prediction.shape[1] > 0:
        emotion_categories = ['feliz', 'triste', 'neutro']
        emocion = emotion_categories[np.argmax(emotion_prediction[0])]
    else:
        emocion = "Desconocido"

    from google.cloud import vision
    vision_client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    colors = []
    try:
        color_response = vision_client.image_properties(image=image)
        if color_response.image_properties_annotation:
            for color in color_response.image_properties_annotation.dominant_colors.colors[:3]:
                color_rgb = (color.color.red, color.color.green, color.color.blue)
                color_name = map_rgb_to_color_name(color_rgb)
                if color_name not in colors and is_valid_color(color_rgb[0], color_rgb[1], color_rgb[2]):
                    colors.append(color_name)
    except Exception as e:
        colors = []

    color_principal = colors[0] if colors else "Desconocido"

    colors_by_category = {
        "tren_superior": [colors[0]] if len(colors) > 0 and upper_clothing else [],
        "tren_inferior": [colors[1]] if len(colors) > 1 and lower_clothing else [],
        "calzado": [colors[2]] if len(colors) > 2 and footwear else []
    }

    if not (upper_clothing or lower_clothing or footwear):
        return None, None, None, [], emocion, {'error': 'No se detectó prenda o vestimenta alguna.'}, None, {}

    logging.debug(f"Upper clothing: {upper_clothing}")
    logging.debug(f"Lower clothing: {lower_clothing}")
    logging.debug(f"Footwear: {footwear}")
    logging.debug(f"Detected colors: {colors}")
    logging.debug(f"Detected emotion: {emocion}")
    logging.debug(f"Predicted category (original): {predicted_category}")

    return upper_clothing, lower_clothing, footwear, colors, emocion, None, color_principal, colors_by_category

def validar_foto(ropa_detectada, genero, lugar, actividad):
    reglas = REGLAS_MODA.get(lugar, {}).get(actividad, {})
    if not reglas or not reglas.get("validacion_foto", {}).get("requiere_persona", False):
        return "No hay reglas de validación para este contexto."
    
    validacion = reglas["validacion_foto"]
    ropa_minima = validacion["ropa_minima"].get(genero, [])
    
    if not ropa_detectada:
        return validacion["mensaje_error"]
    
    for prenda in ropa_minima:
        if prenda not in ropa_detectada:
            return validacion["mensaje_error"]
    
    return "Validación exitosa: ropa mínima cumplida."
import random

try:
    reglas_path = Path("reglas.json")
    if reglas_path.exists():
        with open(reglas_path, encoding="utf-8") as f:
            REGLAS_MODA = json.load(f)
    else:
        logging.error("reglas.json no encontrado. Usando reglas vacías.")
        REGLAS_MODA = {}
except (FileNotFoundError, json.JSONDecodeError) as e:
    logging.error(f"Error al cargar reglas.json: {e}")
    REGLAS_MODA = {}

def flatten_prendas(prendas_dict):
    """Aplana las categorías de prendas en una lista única."""
    flattened = []
    if isinstance(prendas_dict, dict):
        for categoria in prendas_dict.values():
            if isinstance(categoria, dict):
                for subcategoria in categoria.values():
                    flattened.extend(subcategoria)
            elif isinstance(categoria, list):
                flattened.extend(categoria)
    elif isinstance(prendas_dict, list):
        flattened.extend(prendas_dict)
    return flattened

def is_valid_color(r, g, b):
    """Filtra colores muy oscuros o muy claros (evita blanco y negro puro)."""
    if (r > 245 and g > 245 and b > 245) or (r < 15 and g < 15 and b < 15):
        return False
    return True

def map_rgb_to_color_name(rgb):
    """Mapea un color RGB a su nombre más cercano."""
    color_dict = {
        "negro": (0, 0, 0),
        "blanco": (255, 255, 255),
        "gris": (128, 128, 128),
        "rojo": (255, 0, 0),
        "verde": (0, 255, 0),
        "azul": (0, 0, 255),
        "amarillo": (255, 255, 0),
        "marron": (139, 69, 19),
        "naranja": (255, 165, 0),
        "rosado": (255, 192, 203),
        "purpura": (128, 0, 128),
        "trigo": (245, 222, 179),
        "bronce": (205, 127, 50),
        "turquesa": (64, 224, 208),
        "vino": (128, 0, 32),
        "dorado": (255, 215, 0),
        "plata": (192, 192, 192)
    }
    def distancia(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5
    return min(color_dict, key=lambda c: distancia(rgb, color_dict[c]))

def validar_combinacion(lugar, evento, genero, tipo_cuerpo):
    if lugar not in LUGARES:
        return False, f"Lugar '{lugar}' no válido"
    if evento not in LUGARES[lugar]["eventos"]:  # Cambiar EVENTOS por LUGARES
        return False, f"Evento '{evento}' no válido para '{lugar}'"
    if genero not in GENEROS:
        return False, f"Género '{genero}' no válido"
    if tipo_cuerpo not in TIPOS_CUERPO[genero]:
        return False, f"Tipo de cuerpo '{tipo_cuerpo}' no válido para '{genero}'"
    return True, "Combinación válida"

def validar_foto(ropa_detectada, genero, lugar, evento):
    reglas = REGLAS_MODA.get(lugar, {}).get(evento, {})
    if not reglas or not reglas.get("validacion_foto", {}).get("requiere_persona", False):
        return "No hay reglas de validación para este contexto."
    
    validacion = reglas["validacion_foto"]
    ropa_minima = validacion.get("ropa_minima", []).get(genero, [])
    
    if not ropa_detectada:
        return validacion["mensaje_error"]
    
    for prenda in ropa_minima:
        if prenda not in ropa_detectada:
            return validacion["mensaje_error"]
    
    return "Validación exitosa: ropa mínima cumplida."
def generar_evaluacion(lugar, evento, genero, emocion, tipo_cuerpo, outfit):
    analisis_general = []
    puntos_fuerte = []
    puntos_debiles = []
    areas_mejora = []

    if lugar in REGLAS_MODA and evento in REGLAS_MODA[lugar]:
        reglas = REGLAS_MODA[lugar][evento]
        colores_apropiados = reglas.get("colores", {})
        colores_evitados = reglas.get("colores_evitados", {})
        materiales = reglas.get("materiales", [])
        prendas_recomendadas = reglas["prendas_recomendadas"].get(genero, {})
        emocion_data = reglas.get("emocion_recomendaciones", {}).get(emocion, {})
        tipo_cuerpo_data = reglas.get("tipo_cuerpo_recomendaciones", {}).get(genero, {}).get(tipo_cuerpo, "")

        upper_clothing = outfit.get("upper_clothing", [])
        lower_clothing = outfit.get("lower_clothing", [])
        footwear = outfit.get("footwear", [])
        colors_by_category = outfit.get("colors_by_category", {})
        material = outfit.get("material", "desconocido")

        # Análisis general
        analisis_general.append(f"Evaluación para {EVENTOS[evento]} en {LUGARES[lugar]['nombre']} para {genero}, emoción {emocion}, tipo de cuerpo {tipo_cuerpo}.")
        categorias_detectadas = {"tren_superior": upper_clothing, "tren_inferior": lower_clothing, "calzado": footwear}
        if all(any(prenda in flatten_prendas(prendas_recomendadas.get(cat, {})) for prenda in categorias_detectadas[cat]) for cat in ["tren_superior", "tren_inferior", "calzado"]):
            analisis_general.append("El outfit es completamente adecuado para el contexto.")
        elif any(prenda not in flatten_prendas(prendas_recomendadas.get(cat, {})) for cat in ["tren_superior", "tren_inferior", "calzado"] for prenda in categorias_detectadas[cat]):
            analisis_general.append("El outfit tiene elementos no adecuados para el contexto.")

        # Puntos fuertes
        for cat, prendas in [("tren_superior", upper_clothing), ("tren_inferior", lower_clothing), ("calzado", footwear)]:
            for prenda in prendas:
                if prenda in flatten_prendas(prendas_recomendadas.get(cat, {})):
                    puntos_fuerte.append(f"{prenda.capitalize()} en {cat} es apropiado para el evento.")
            colors_cat = colors_by_category.get(cat, [])
            if any(color in colores_apropiados.get(cat, []) for color in colors_cat):
                puntos_fuerte.append(f"Colores {', '.join([c for c in colors_cat if c in colores_apropiados.get(cat, [])])} en {cat} son adecuados.")
        if material in materiales:
            puntos_fuerte.append(f"Material {material} es adecuado para el clima y el evento.")
        for cat in ["tren_superior", "tren_inferior", "calzado"]:
            if not outfit.get(cat if cat != "calzado" else "footwear", []):
                puntos_debiles.append(f"No se detectó prenda en {cat.replace('_', ' ')}.")
                sugerencias = flatten_prendas(prendas_recomendadas.get(cat, {}))
                if sugerencias:
                    areas_mejora.append(f"Puedes considerar usar: {', '.join(sugerencias[:3])}.")

        # Puntos débiles
        for cat, prendas in [("tren_superior", upper_clothing), ("tren_inferior", lower_clothing), ("calzado", footwear)]:
            for prenda in prendas:
                if prenda not in flatten_prendas(prendas_recomendadas.get(cat, {})):
                    puntos_debiles.append(f"{prenda.capitalize()} en {cat} no es adecuado para '{reglas['formalidad']}'.")
            colors_cat = colors_by_category.get(cat, [])
            if any(color in colores_evitados.get(cat, []) for color in colors_cat):
                puntos_debiles.append(f"Colores {', '.join([c for c in colors_cat if c in colores_evitados.get(cat, [])])} en {cat} deben evitarse.")
        if material not in materiales:
            puntos_debiles.append(f"Material {material} no es ideal para el evento.")
        if tipo_cuerpo_data and any(prenda not in flatten_prendas(prendas_recomendadas.get(cat, {})) for cat in ["tren_superior", "tren_inferior"] for prenda in categorias_detectadas[cat]):
            puntos_debiles.append(f"El outfit no favorece el tipo de cuerpo {tipo_cuerpo}: {tipo_cuerpo_data}.")

        for cat, prendas in [("tren_superior", upper_clothing), ("tren_inferior", lower_clothing), ("calzado", footwear)]:
            for prenda in prendas:
                if prenda not in flatten_prendas(prendas_recomendadas.get(cat, {})):
                    areas_mejora.append(f"Reemplaza {prenda} en {cat} por {prendas_recomendadas.get(cat, [''])[0]}.")
            colors_cat = colors_by_category.get(cat, [])
            if any(color in colores_evitados.get(cat, []) for color in colors_cat):
                areas_mejora.append(f"Usa colores como {', '.join(colores_apropiados.get(cat, [])[:2])} en {cat}.")
        if emocion_data.get("sugerencia_color"):
            areas_mejora.append(f"Considera {', '.join(emocion_data['sugerencia_color'])} para reflejar {emocion}.")
        if tipo_cuerpo_data and any(prenda not in flatten_prendas(prendas_recomendadas.get(cat, {})) for cat in ["tren_superior", "tren_inferior"] for prenda in categorias_detectadas[cat]):
            areas_mejora.append(f"Ajusta {cat} según {tipo_cuerpo_data}.")

    return {
        "analisis_general": " ".join(analisis_general),
        "puntos_fuerte": puntos_fuerte,
        "puntos_debiles": puntos_debiles,
        "areas_mejora": areas_mejora
    }

def filtrar_si_hay_suficientes(prendas, keywords, minimo=3):
    """Filtra solo si hay suficientes coincidencias, si no, devuelve la lista original."""
    filtradas = [p for p in prendas if any(k in p.lower() for k in keywords)]
    return filtradas if len(filtradas) >= minimo else prendas

def recommend_items(lugar, evento, genero="mujeres", tipo_cuerpo="sin_tipo", emocion="neutro", armario_id=None):
    recomendaciones = {
        "tren_superior": [],
        "tren_inferior": [],
        "calzado": [],
        "notas_armario": [],
        "mas_recomendaciones_url": f"/generate_more?lugar={lugar}&evento={evento}&genero={genero}&tipo_cuerpo={tipo_cuerpo}&emocion={emocion}"
    }

    if tipo_cuerpo not in TIPOS_CUERPO[genero]:
        tipo_cuerpo = "sin_tipo"
    if emocion not in ["feliz", "triste", "neutro"]:
        emocion = "neutro"

    try:
        sugerencias_base = RECOMENDACIONES_AVANZADAS["recomendaciones_por_lugar_evento"][lugar][evento][genero]
        sugerencias = {
            "tren_superior": sugerencias_base["tren_superior"].copy(),
            "tren_inferior": sugerencias_base["tren_inferior"].copy(),
            "calzado": sugerencias_base["calzado"].copy()
        }

        # Filtros por emoción
        if emocion == "feliz":
            sugerencias["tren_superior"] = filtrar_si_hay_suficientes(sugerencias["tren_superior"], ["elegante", "ligera", "detalles"])
            sugerencias["tren_inferior"] = filtrar_si_hay_suficientes(sugerencias["tren_inferior"], ["fluida", "elegante", "midi"])
            sugerencias["calzado"] = filtrar_si_hay_suficientes(sugerencias["calzado"], ["elegante", "decorada", "cuña"])
        elif emocion == "triste":
            sugerencias["tren_superior"] = filtrar_si_hay_suficientes(sugerencias["tren_superior"], ["oscura", "sencilla"])
            sugerencias["tren_inferior"] = filtrar_si_hay_suficientes(sugerencias["tren_inferior"], ["oscura", "sencilla"])
            sugerencias["calzado"] = filtrar_si_hay_suficientes(sugerencias["calzado"], ["oscuro", "sencillo"])

        if tipo_cuerpo == "reloj_arena":
            sugerencias["tren_superior"] = filtrar_si_hay_suficientes(sugerencias["tren_superior"], ["ajustada", "vestido", "ceñido", "entallado", "top"])
            sugerencias["tren_inferior"] = filtrar_si_hay_suficientes(sugerencias["tren_inferior"], ["ajustada", "midi", "entallada"])
        elif tipo_cuerpo == "triangulo_pera":
            sugerencias["tren_superior"] = filtrar_si_hay_suficientes(sugerencias["tren_superior"], ["detalles", "volumen", "escote"])
            sugerencias["tren_inferior"] = filtrar_si_hay_suficientes(sugerencias["tren_inferior"], ["fluida", "ancha", "liviana"])

        for categoria in ["tren_superior", "tren_inferior", "calzado"]:
            opciones = sugerencias.get(categoria, [])
            if len(opciones) >= 3:
                recomendaciones[categoria].extend(random.sample(opciones, 3))
            elif opciones:
                seleccionadas = opciones.copy()
                while len(seleccionadas) < 3:
                    seleccionadas.append(random.choice(opciones))
                recomendaciones[categoria].extend(seleccionadas)

    except KeyError as e:
        logging.error(f"No se encontraron recomendaciones para lugar: {lugar}, evento: {evento}, género: {genero}. Error: {e}")
        return recomendaciones

    try:
        armario_path = Path("armario_digital.json")
        if armario_id and armario_path.exists():
            with open(armario_path, encoding="utf-8") as f:
                ARMARIOS = json.load(f)
            if armario_id in ARMARIOS:
                armario = ARMARIOS[armario_id][genero]
                upper_armario = flatten_prendas(armario.get("tren_superior", {}))
                lower_armario = flatten_prendas(armario.get("tren_inferior", {}))
                footwear_armario = flatten_prendas(armario.get("calzado", {}))

                for prenda in recomendaciones["tren_superior"]:
                    if prenda in upper_armario:
                        recomendaciones["notas_armario"].append(f"La prenda superior '{prenda}' está en tu armario.")
                for prenda in recomendaciones["tren_inferior"]:
                    if prenda in lower_armario:
                        recomendaciones["notas_armario"].append(f"La prenda inferior '{prenda}' está en tu armario.")
                for prenda in recomendaciones["calzado"]:
                    if prenda in footwear_armario:
                        recomendaciones["notas_armario"].append(f"El calzado '{prenda}' está en tu armario.")
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logging.error(f"Error al cargar o procesar armario_digital.json: {e}")

    return recomendaciones

@app.route('/lugares', methods=['GET'])
def get_lugares():
    return jsonify({"lugares": list(LUGARES.keys())})

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/api/recomendaciones', methods=['POST'])
def get_recomendaciones():
    data = request.get_json()
    lugar = data.get('lugar')
    evento = data.get('evento')
    genero = data.get('genero')
    tipo_cuerpo = data.get('tipo_cuerpo', '')

    print(f"Recibido: lugar={lugar}, evento={evento}, genero={genero}, tipo_cuerpo={tipo_cuerpo}")
    print(f"Validando: lugar={lugar}, evento={evento}, genero={genero}, tipo_cuerpo={tipo_cuerpo}")
    print(f"LUGARES: {LUGARES.keys()}")
    print(f"Eventos para {lugar}: {LUGARES[lugar]['eventos']}")
    print(f"Generos: {GENEROS}")
    print(f"Tipos de cuerpo para {genero}: {TIPOS_CUERPO[genero]}")
    # Validación paso a paso
    if lugar not in LUGARES:
        print(f"Lugar '{lugar}' no válido")
        return jsonify({'error': f"Lugar '{lugar}' no válido"}), 400
    if evento not in LUGARES[lugar]["eventos"]:
        print(f"Evento '{evento}' no válido para '{lugar}'")
        return jsonify({'error': f"Evento '{evento}' no válido para '{lugar}'"}), 400
    if genero not in GENEROS:
        print(f"Género '{genero}' no válido")
        return jsonify({'error': f"Género '{genero}' no válido"}), 400
    if tipo_cuerpo not in TIPOS_CUERPO[genero]:
        print(f"Tipo de cuerpo '{tipo_cuerpo}' no válido para '{genero}'")
        return jsonify({'error': f"Tipo de cuerpo '{tipo_cuerpo}' no válido para '{genero}'"}), 400

    print("Validación exitosa")
    valido, mensaje = validar_combinacion(lugar, evento, genero, tipo_cuerpo)
    print(f"Validación: {valido}, Mensaje: {mensaje}")

    if not valido:
        return jsonify({'error': mensaje}), 400

    # Obtener recomendaciones
    recomendaciones = recommend_items(lugar, evento, genero, tipo_cuerpo)
    
    # Enviar las recomendaciones como respuesta
    return jsonify({"recomendaciones": recomendaciones})


@app.route('/analizar-imagen', methods=['POST'])
def analizar_imagen():
    if 'image' not in request.files:
        return jsonify({"error": "No se subió imagen"}), 400

    image = request.files['image']
    image_content = image.read()
    lugar = request.form.get('lugar', 'espacio_diario')
    evento = request.form.get('evento', 'general')
    genero = request.form.get('genero', 'mujeres')
    tipo_cuerpo = request.form.get('tipo_cuerpo', 'sin_tipo')

    is_valid, message = validar_combinacion(lugar, evento, genero, tipo_cuerpo)
    if not is_valid:
        return jsonify({"error": message}), 400

    try:
        upper_clothing, lower_clothing, footwear, colors, emocion, warning, color_principal, colors_by_category = detect_clothing(image_content)
    except Exception as e:
        logging.error(f"Error en detect_clothing: {e}")
        return jsonify({"error": "Error al procesar la imagen"}), 500

    if warning:
        logging.warning(f"Advertencia detectada: {warning}")
        return jsonify({"error": warning}), 400

    ropa_detectada = upper_clothing + lower_clothing + footwear
    validacion = validar_foto(ropa_detectada, genero, lugar, evento)
    if "error" in validacion.lower():
        return jsonify({"error": validacion}), 400

    outfit = {
        "upper_clothing": upper_clothing,
        "lower_clothing": lower_clothing,
        "footwear": footwear,
        "colores": colors,
        "colors_by_category": colors_by_category,
        "material": "desconocido"
    }

    evaluacion = generar_evaluacion(
    lugar=lugar,
    evento=evento,
    genero=genero,
    emocion=emocion,
    tipo_cuerpo=tipo_cuerpo,
    outfit=outfit
    )
    return jsonify({
        "detected_clothing": {
            "tren_superior": upper_clothing,
            "tren_inferior": lower_clothing,
            "calzado": footwear
        },
        "detected_colors": colors,
        "colors_by_category": colors_by_category,
        "detected_emocion": emocion,
        "color_principal": color_principal,
        "validacion": validacion,
        "evaluacion": evaluacion
    })
@app.route('/evaluar-outfit', methods=['POST'])
def evaluar_outfit():
    data = request.json
    lugar = data.get('lugar')
    evento = data.get('evento')
    genero = data.get('genero')
    emocion = data.get('emocion')
    tipo_cuerpo = data.get('tipo_cuerpo')
    outfit = data.get('outfit', {})

    if not all([lugar, evento, genero, emocion, tipo_cuerpo]):
        return jsonify({"error": "Faltan parámetros: lugar, evento, genero, emocion, tipo_cuerpo"}), 400

    is_valid, message = validar_combinacion(lugar, evento, genero, tipo_cuerpo)
    if not is_valid:
        return jsonify({"error": message}), 400

    evaluacion = generar_evaluacion(lugar, evento, genero, emocion, tipo_cuerpo, outfit)
    return jsonify(evaluacion)
@app.route('/api/recomendaciones', methods=['OPTIONS'])
def handle_options():
    response = jsonify({'message': 'OK'})
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:8000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    return response



@app.route('/api/lugares_eventos', methods=['GET'])
def lugares_eventos():
    with open('recomendaciones.json', encoding='utf-8') as f:
        data = json.load(f)
    lugares_eventos = {}
    for lugar, contenido in data["recomendaciones_por_lugar_evento"].items():
        eventos = list(contenido.keys())
        lugares_eventos[lugar] = eventos
    for lugar in ["espacio_publico", "salida_nocturna", "espacio_laboral", "restaurante_bar", "espacio_diario", "gimnasio_parque", "iglesia"]:
        if lugar in data:
            if "eventos" in data[lugar]:
                lugares_eventos[lugar] = data[lugar]["eventos"]
            else:
                eventos = [k for k in data[lugar].keys() if k != "nombre" and k != "eventos"]
                lugares_eventos[lugar] = eventos
    return jsonify(lugares_eventos)
if __name__ == '__main__':
    app.run(debug=True)