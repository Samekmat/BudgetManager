from functools import wraps
from typing import Optional


def keep_parameters(cls):
    """A decorator to add request parameters to the context data of a Django class-based
    view."""

    @wraps(cls, updated=())
    class Wrapper(cls):
        def get_context_data(self, *, object_list: Optional[list] = None, **kwargs) -> dict:
            """Adds request parameters to the context data.

            Args:
            - object_list (Optional[list]): List of objects.
            - **kwargs: Additional keyword arguments.

            Returns:
            - dict: The context data with added parameters.
            """

            _request_copy = self.request.GET.copy()
            parameters = _request_copy.pop("page", True) and _request_copy.urlencode()
            context = super().get_context_data(**kwargs)
            context["parameters"] = parameters
            return context

    return Wrapper
