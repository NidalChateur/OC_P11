from club_app.models.club import Club


def get_all_activated_clubs():
    return Club.query.filter_by(is_activated=True).all()
