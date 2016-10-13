from django.conf.urls import url
from .views import handle, service_root

urlpatterns = [
		url(r'^$', service_root, name='odata_service_root'),
    url(r'^(?P<odata_path>.+)$', handle, name='odata_request_handler')
]