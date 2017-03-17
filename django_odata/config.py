from django.conf import settings

def get_entity_sets_list():
  """
  Returns the list of Entity Sets as configured
  in the application DJANGO_ODATA['sets']
  """
  sets = settings.DJANGO_ODATA['sets']
  return sets.keys()
