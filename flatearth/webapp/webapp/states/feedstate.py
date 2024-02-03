from ..imports import *
from flatearth.models import Feed
from .userstate import UserState

class FeedState(UserState):
    # seen_json: str = '[]'
    # read_json: str = '[]'
    pending_json: str = '{}'
    seen_json: str = rx.LocalStorage('[]')
    read_json: str = rx.LocalStorage('[]')
    # pending_json: str = rx.LocalStorage('[]')
    max_queue_size: int = 50

    @rx.var
    def seen(self): return set(from_json(self.seen_json))
    @rx.var
    def read(self): return set(from_json(self.read_json))
    @rx.var
    def pending(self): return from_json(self.pending_json)
    @rx.var
    def pending_ids(self): return set(self.pending.keys())
    @rx.var
    def num_pending(self): return len(self.pending)
    
    def mark_read(self, post_id_or_ids:int|set|list):
        post_ids = {post_id_or_ids} if type(post_id_or_ids)==int else set(post_id_or_ids)
        logger.debug(f'marking as read: {post_ids}')
        # anything new?
        if post_ids - self.seen:
            self.seen_json = to_json(list(self.seen|post_ids))
            self.pending_json = to_json({
                id:d
                for id,d in self.pending.items()
                if int(id) not in post_ids
            })
    
    @rx.background
    async def check_feed(self):
        while True:
            if self.num_pending < self.max_queue_size:
                logger.debug(f'{self.num_pending} pending: {self.pending_ids}')
                logger.debug(f'checking feed for user {self.username}')
                feed = Feed(user_id=self.user_id)
                posts = feed.latest(
                    n=(self.max_queue_size*1.5) - self.num_pending,
                    seen=self.seen|self.pending_ids,
                )
                async with self:
                    data = {
                        **self.pending,
                        **{
                            str(post.id):post.data
                            for post in posts
                        },
                    }
                    logger.debug(f'now have {len(data)} pending')
                    self.pending_json = to_json(data)

            await asyncio.sleep(10)