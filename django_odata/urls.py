from django.conf.urls import url
from .views import handle_request, service_root

urlpatterns = [
  # Service description handler
  url(r'^$', 
    service_root, 
    name='odata_service_root'),
  # Request handler
  url(r'^(?P<odata_path>.+)$', 
    handle_request, 
    name='odata_request_handler')
]