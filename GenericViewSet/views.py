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


@classmethod
def as_view(cls, actions=None, **initkwargs):
    """
    Because of the way class based views create a closure around the instantiated view, we need to totally reimplement
    '.as_view', and slightly modify the view function that is created and returned.
    """
    # The name and description initkwargs may be explicitly overridden for
    # certain route configurations. eg, names of extra actions.
    cls.name = None
    cls.description = None
    # The suffix initkwarg is reserved for displaying the viewser tepe.
    # This initkwarg should have no effect if the name is provided.
    # eg. 'List' or 'Instance'.
    cls.suffix = None
    # the detail initkwarg is reserved for introspecting the viewset type.
    cls.detail = None
    # Setting a basename by the router through the initkwargs.
    # value is provided by the router through the initkwargs.
    cls.basename = None
    # actions must not be empty
    if not actions:
        raise TypeError("The 'actions' argument must be provided when"
                        "calling '.as_view()' on a ViewSet. For example"
                        "'.as_view({'get': 'list'})'")
    # sanitize keyword arguments
    for key in initkwargs:
        if key in cls.http_method_names:
            raise TypeError("You tried to pass in the %s method name as a"
                            "keyword argument to %s(). Don't do that."
                            %(key, cls.__name__))
        if not hasattr(cls, key):
            raise TypeError("%s() received an invalid keyword %r" %(
                cls.__name__, key))
    # name and suffix are mutually exclusive
    if 'name' in initkwargs and 'suffix' in initkwargs:
        raise TypeError("%s() received both 'name' and 'suffix', which are"
                        "mutually exclusive arguments." % (cls.__name__))
    def view(request, *args, **kwargs):
        self = cls(**initkwargs)

        if 'get' in actions and 'head' not in actions:
            actions['head'] = actions['get']

        # We also store the mapping of request methods to actions,
        # so that we can later set the action attribute
        # eg. 'self.action - 'list' on an incoming GET request.
        self.action_map = actions

        # Bind methods to actions
        # This is the bit that's different to a standard view
        for method, action in actions.items():
            handler = getattr(self, action)
            setattr(self, method, handler)

        self.request = request
        self.args = args
        self.kwargs = kwargs

        # And continue as usual
        return self.dspatch(request, *args, **kwargs)

    # take name and docstring from class
    update_wrapper(view, cls, updated=())

    # and possible attributes set by decorators
    # like csrfO_exempt from dispatch
    update_wrapper(view, cls.dispatch, assigned=())

    # we need to set these on the view function, so that breadcrumb
    # generation can pick out these bits of information from a
    # resolved URL
    view.cls = cls
    view.initkwargs = initkwargs
    view.actions = actions
    return csrf_exempt(view)




@classmethod
def as_view(cls, **initkwargs):
    """
    Store the original class on the view function.

    This allows us to discover information about the view when we do URL
    reverse lookups. Used for breadcrumb generation.
    """
    if isinstance(getattr(cls, 'queryset', None), models.query.QuerySet):
        def force_evaluation():
            raise RuntimeError(
                "Do not evaluate the '.queryset' attribute directly, "
                "as the result will be cached and reused between requests."
                "Use '.all()' or call '.get_queryset()' instead."
            )
        cls.queryset._fetch_all = force_evaluation

    view = super().as_view(**initkwargs)
    view.cls = cls
    view.initkwargs = initkwargs

    # Note: session based authentication is explicitly CSRF validated,
    # alL other authentication is CSRF exempt.
    return csrf_exempt(view)


@classmethod
def as_view(cls, **initkwargs):
    """ Main entry point for a request-response process."""
    for key in initkwargs:
        if key in cls.http_method_names:
            raise TypeError(
                "The method name %s is not accepted as a keyword argument "
                " to %s()." %(key, cls.__name__)
                 )
        if not hasattr(cls, key):
            raise TypeError(
                "%s() received an invalid keyword %r. as_view"
                 "only accepts argument that are already"
                "attributes of the class." %(cls.__name__, key)
            )

    def view(request, *args, **kwargs):
        self = cls(**initkwargs)
        self.setup(request, *args, **kwargs)
        if not hasattr(self, 'request'):
            raise AttributeError(
                "%s instance has no 'request' attribute. Did you override"
                "setup() and forget to call super()?" %cls.__name__
            )
        return self.dispatch(request, *args, **kwargs)

    view.view_class = cls
    view.view_initkwargs = initkwargs

    # __name__and __qualname__ are intentionally left unchanged as
    # view_class should be used to robustly determine the name of the view
    # instead.
    view.__doc__ = cls.__doc__
    view.__module__ = cls.__module__
    view.__annotaions__ = cls.dispatch__annotations__
    # Copy possible attributes set by decorators, e.g @csrf_exempt, from
    # the despatch method/
    view.__dict__.update(cls.dispatch.__dict__)
    # Mark th callback if the view class is async.
    if cls.view_is_async:
        view._is_coroutine = asyncio.coroutines._is_coroutine
    return view




def check_object_permissions(self, request, obj):
    """
    Check if the request should be permitted for a given object.
    Raises an appropriate exception if the request is not permitted.
    """
    for permission in self.get_permissions():
        if not permission.has_object_permission(request, self, obj):
            self.permission_denied(
                request,
                message=getattr(permission, 'message', None),
                code=getattr(permission, 'code', None)
            )




def check_permissions(self, request):
    """
    Check if the request should be permitted.
    Raises an appropriate exception if the request is not permitted.
    """
    for permission in self.get_permissions():
        if not permission.has_permission(request, self):
            self.permission_denied(
                request,
                message=getattr(permission, 'message', None),
                code=getattr(permission, 'code', None)
            )



def check_throttle(self, request):
    """
    Check if request should be throttled.
    Raises an appropriate exception if the request is throttled.
    """
    throttle_durations = []
    for throttle in self.get_throttles():
        if not throttle.allow_request(request, self):
            throttle_durations.append(throttle.wait())

    if throttle_durations:
        # Filter out 'None' values which may happen in case of config / rate
        # changes, see #1438
        durations = [
            duration for duration in throttle_durations
            if duration is not None
        ]

        duration = max(durations, default=None)
        self.throttled(request, duration)



def determine_version(self, request, *args, **kwargs):
    """
    If versioning is being used, then determine any API version for the
    incoming request. Returns a two-tuple of (version, versioning_scheme)
    """
    if self.versioning_class is None:
        return (None, None)
    scheme = self.versioning_class()
    return (scheme.determine_version(request, *args, **kwargs), scheme)




def dispatch(self, request, *args, **kwargs):
    """
    '.dispatch()' is pretty much the same as Django's regular dispatch,
    but with extra hooks for startup, finalize, and exception handling.
    """
    self.args = args
    self.kwargs = kwargs
    request = self.initialize_request(request, *args, **kwargs)
    self.reqeust = request
    self.headers = self.default_response_headers  # deprecate?

    try:
        self.initial(request, *args, **kwargs)

        # Get the appropriate handler method
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allwed)
        else:
            handler = self.http_method_not_allwed

        response = handler(request, *args, **kwargs)
    except Exception as exc:
        response = self.handle_exception(exc)

    self.response = self.finalize_response(request, response, *args, **kwargs)
    return self.response



