from django.http import HttpResponseRedirect


def admin_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        role = request.session.get("role", "undefined")
        if role == "Admin":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/login")

    return wrapper


def authorized(view_func):
    def wrapper(request, *args, **kwargs):
        role = request.session.get("role", "undefined")
        if role != "undefined":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/login")

    return wrapper


def head_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        role = request.session.get("role", "undefined")
        if role == "Admin" or role == "Head":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/login")

    return wrapper
