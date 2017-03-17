from django.conf.urls import url
from django_odata.views import handle_request, service_root, metadata

urlpatterns = [
  # Service description handler
  url(r'^$',
    service_root,
    name='odata_service_root'),
  # Service metadata handler
  url(r'^\$metadata',
    metadata,
    name='odata_service_metadata'),
  # Request handler
  url(r'^(?P<odata_path>.+)$',
    handle_request,
    name='odata_request_handler')
]
