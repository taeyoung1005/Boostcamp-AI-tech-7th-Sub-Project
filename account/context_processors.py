def user_profile(request):
    if request.user.is_authenticated:
        return {
            "username": request.user.username,
            "profile_image": request.user.profile_image,
        }
    else:
        return {
            "username": None,
            "profile_image": None,
        }
