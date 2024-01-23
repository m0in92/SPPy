from django.urls import path, re_path
from . import views


app_name: str = 'sppy'
urlpatterns: list = [
    path(route='', view=views.index, name='index'),
    re_path(route=r"^api/batterysim/sp$", view=views.SpParamView.as_view(), name='sp_sv_set'),
    re_path(route=r"^api/batterysim/ecm$", view=views.EcmParamView.as_view(), name='ecm_sv_set')

]