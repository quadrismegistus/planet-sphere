from ..imports import *
from .post import *
from .user import *

NUM_LATEST = 10

class Feed:
    def __init__(self, user_id=None, user=None, **user_q):
        if user or user_id or user_q:
            if user_id: user_q['id']=user_id
            self.user = user if user else User.get(**user_q)
    
    def latest(self, 
            n:int=NUM_LATEST, 
            as_json:bool=False, 
            seen:Optional[set]=None, 
            only_following:bool=False,
            incl_replies:bool=True,
            incl_reposts:bool=True,
            **kwargs):
        
        # begin query
        q = get_db_session().query(Post)
        
        # seen already?
        if seen: 
            q=q.filter(Post.id.not_in(set(seen)))

        # following?
        if only_following:
            q=q.filter(Post.user_id.in_(self.user.following_ids))    
        
        # replies?
        if not incl_replies: 
            q=q.filter(Post.replying_to==None)
        
        # reposts?
        if not incl_reposts: 
            q=q.filter(Post.reposting==None)

        # sort
        q=q.order_by(-Post.timestamp)

        # limit
        q=q.limit(n)

        # get
        res=q.all()

        # return
        return self.as_json(res) if as_json else res
    
    @classmethod
    def as_json(self, posts):
        return to_json([post.data for post in posts])