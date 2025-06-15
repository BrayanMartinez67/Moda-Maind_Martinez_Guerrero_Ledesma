from django.urls import path
from Authentication.Views import views_login
from Assessment.views import views
from Assessment.views.views import evaluacion_formulario

urlpatterns = [
    path('', views_login.home_view, name='home'),
    path('signup/', views_login.signup_view, name='signup'),
    path('signin/', views_login.signin_view, name='signin'),
    path('logout/', views_login.logout_view, name='logout'),
    path('inicio/', views.subir_outfit, name='inicio'),
    path('evaluacion/', evaluacion_formulario, name='evaluacion_formulario'),
    path('reset/request/', views_login.request_reset_view, name='password_reset_custom'),
    path('reset/code/', views_login.verify_code_view, name='verify_code'),
    path('reset/new/', views_login.set_new_password_view, name='set_new_password'),
]
