#abdul add decorators

from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def user_passes_test(test_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print('start test....')
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Error: Tier 12 access required...')
                request.session['error_message'] = 'Error: Tier 12 access required...'
                # Redirect to the success URL or a default URL
                return redirect(request.META.get('HTTP_REFERER', 'default_success_url'))

        return _wrapped_view

    return decorator

def is_persona_tier_12(user):
    return user.is_authenticated and user.ruser_account.first().user_persona.persona_tier == 12