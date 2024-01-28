from .post import *

class Feed:
    def __init__(self, user):
        self.user = user

    def latest(self):
        return get_db_session().query(
            Post
        ).filter(
            Post.user_id.in_(self.user.following_ids)
        ).order_by(
            Post.timestamp.desc()
        ).all()