from django.core.exceptions import ObjectDoesNotExist

def detect_user(user):
    if user.role.role == 'admin':
        redirect_url = 'accounts:dashboard_eval'
    elif user.role.role == 'TA':
        try:
            if user.teachingassistantprofile:
                redirect_url = 'pengisianLog:daftar_log_ta'
        except ObjectDoesNotExist:
            redirect_url = 'accounts:fill_profile'
    else:
        redirect_url = 'authentication:not_assign'

    return redirect_url