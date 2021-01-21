def display_name(active_user):
    if active_user.is_authenticated:
        if active_user.nick:
            display_name = active_user.nick
        else:
            display_name = active_user.first_name

        return display_name
    return None
