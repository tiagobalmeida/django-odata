from django_odata.views import handle_request
from django.conf.urls import url
"""
This urlconf exists because Django expects ROOT_URLCONF to exist. URLs
should be added within the test folders, and use TestCase.urls to set them.
This helps the tests remain isolated.
"""

urlpatterns = [
  # Service description handler
  #url(r'^$',
  #  service_root,
  #  name='odata_service_root'),
  # Service metadata handler
  #url(r'^\$metadata',
  #  metadata,
  #  name='odata_service_metadata'),
  # Request handler
  url(r'^(?P<odata_path>.+)$',
    handle_request,
    name='odata_request_handler')
]