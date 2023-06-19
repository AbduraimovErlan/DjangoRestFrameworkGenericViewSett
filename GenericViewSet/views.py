from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet

"""
allowed_methods = property object
authentication_classes = [<class '
content_negotiation_class = <class
default_response_headers = property object
filter_backends = []
http_method_names = []
lookup_field = 'pk'
lookup_url_kwarg = None
metadata_class = <class
pagination_class = None
paginator = property object
parser_classes = [
permission_classes = [class
queryset = None
renderer_classes = [class
schema = 
serializer_class = None
settings = 
throttle_classes = []
versioning_class = None
view_is_async = False



"""




def _allowed_methods(self):
    return [m.upper() for m in self.http_method_names if hasattr(self, m)]