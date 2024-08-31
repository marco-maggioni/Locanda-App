from django.urls import path
from . import views

urlpatterns = [
    #path('locandanews/', views.news, name='news'),
	path('locandaform/', views.form_view, name='form_view'),
	path('locandaform/thankyou/<str:mail>/', views.thanks_view, name='thanks'),
	path('locandaform/checkmail', views.checking, name='check'),
    path('locandaform/policy', views.policy, name='policy'),
]