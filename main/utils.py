def detect_user(user):
    if user.role.role == 'admin':
        redirect_url = 'accounts:dashboard_eval'
    elif user.role.role == 'TA':
        redirect_url = 'pengisianLog:daftar_log_ta'
    else:
        redirect_url = 'authentication:not_assign'

    return redirect_url