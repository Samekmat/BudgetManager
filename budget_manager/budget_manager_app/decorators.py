from functools import wraps


def keep_parameters(cls):
    @wraps(cls, updated=())
    class Wrapper(cls):
        def get_context_data(self, *, object_list=None, **kwargs):
            _request_copy = self.request.GET.copy()
            parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
            context = super().get_context_data(**kwargs)
            context['parameters'] = parameters
            return context

    return Wrapper
