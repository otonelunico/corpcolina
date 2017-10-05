from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required


from documents.views import ListPersonalized, ListPersonalizedSet, \
    Resumen, Document_create, Detalle_doc, Create_value, Active_off, Document_list, Document_list_filter, Document_edit, Edit_value, prints

urlpatterns = [
    url(r'^$', login_required(Resumen),name='home'),
    url(r'^nuevo$',login_required(Document_create),name='document_form'),
    url(r'^new/(?P<value>\w+)$',login_required(Create_value),name='create_value'),
    url(r'^editar/(?P<value>\w+)/(?P<id_value>\d+)$',login_required(Edit_value),name='edit_value'),
    url(r'^active_off/(?P<value>\w+)/(?P<id_value>\d+)$',login_required(Active_off), name='active_off'),
    url(r'^list/$', login_required(Document_list), name="documento_list"),
    url(r'^list/personalized/$', login_required(ListPersonalized.as_view()), name="documento_personalized"),
    url(r'^list/personalized/(?P<sere>\w+)/(?P<dere>\w+)/(?P<type>\w+)/(?P<date>\w+)/(?P<null>\w+)/$', login_required(ListPersonalizedSet.as_view()), name="documento_personalized_sel"),
    url(r'^list/(?P<value>\w+)/$', login_required(Document_list_filter), name="documento_list_filter"),
    url(r'^detalle/(?P<id_docum>\d+)$', login_required(Detalle_doc), name="documento_detalle"),
    url(r'^editar/(?P<id_documento>\d+)$', login_required(Document_edit), name="documento_edit"),
    url(r'^resume$', login_required(Resumen), name="resume"),
    url(r'^impreso/(?P<id_docum>\d+)$', login_required(prints), name="documento_impreso"),
    ]