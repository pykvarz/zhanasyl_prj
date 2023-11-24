from django.contrib.auth.decorators import user_passes_test


def root_required(view_func):
    return user_passes_test(lambda u: u.is_root, login_url='/login/')(view_func)


def has_key_user_required(view_func):
    return user_passes_test(lambda u: not u.is_root, login_url='/login/')(view_func)
