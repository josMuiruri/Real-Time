from functools import wraps
from django.core.exceptions import PermissionDenied

def login_required(f):
    '''Protects GraphQL resolvers by blocking unauthenticated requests.'''
    @wraps(f)
    def wrapper(root, info, *args, **kwargs):
        user = info.context.user
        if not user or user.is_anonymous:
            raise PermissionDenied('Authentication token is missing or invalid.')
        return f(root, info, *args, **kwargs)
    return wrapper