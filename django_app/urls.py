from django.urls import path
from . import views


app_name: str = 'sppy'
urlpatterns: list = [
    path(route='', view=views.index, name='index'),
    path(route="batterysim/sp", view=views.sp, name='sp'),
    path(route="batterysim/ecm", view=views.ecm, name='ecm')
]