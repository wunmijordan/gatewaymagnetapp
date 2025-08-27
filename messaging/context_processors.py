from .forms import BulkMessageForm

def bulk_message_form(request):
    """
    Adds a BulkMessageForm instance to the template context
    so the modal can render on any page using base.html.
    """
    return {'bulk_message_form': BulkMessageForm()}
