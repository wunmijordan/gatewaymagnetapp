import threading

_thread_locals = threading.local()

def get_current_user():
    """Return the user for the current request thread, if any."""
    return getattr(_thread_locals, "user", None)

class CurrentUserMiddleware:
    """Store the current logged-in user in thread-local storage."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = getattr(request, "user", None)
        response = self.get_response(request)
        return response
