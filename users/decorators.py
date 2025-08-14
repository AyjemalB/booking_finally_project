from django.http import HttpResponseForbidden

# Разграничение прав доступа
def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role != role:
                return HttpResponseForbidden("Доступ запрещён")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
