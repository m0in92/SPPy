from django.urls import path, re_path
from . import views


app_name: str = 'sppy'
urlpatterns: list = [
    path(route='', view=views.index, name='index'),
    path(route="batterysim/sp", view=views.sp, name='sp'),
    path(route="batterysim/ecm", view=views.ecm, name='ecm'),
    re_path(route=r"^api/batterysim$", view=views.sp_serializer_view_get, name='sp_sv_set')

]