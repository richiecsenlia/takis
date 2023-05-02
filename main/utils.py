def detect_user(user):
    if user.role.role == 'admin':
        redirect_url = 'accounts:dashboard_eval'
        return redirect_url
    elif user.role.role == 'TA':
        redirect_url = 'pengisianLog:daftar_log_ta'
        return redirect_url