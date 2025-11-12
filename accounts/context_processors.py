def user_role(request):
    """Make user role available in all templates"""
    if request.user.is_authenticated:
        return {'user_role': request.user.role}
    return {}