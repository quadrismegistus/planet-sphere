from ..imports import *
from flatearth.models import User, UserNotExist
from .locstate import LocationState

class UserState(LocationState):
    json: dict = rx.LocalStorage('{}')
    username: str = ''
    error: str = ''
    token: str = ''
    logged_in:bool = False

    @rx.var
    def user_id(self) -> int:
        res = self.login_from_token()
        return res.get('sub') if res else 0

    def init(self):
        data=from_json(self.json)
        self.username=data.get('username','')
        self.token = data.get('token')
        if self.token:
            self.login_from_token()

    def login_from_token(self):
        if not self.token: return False
        try:
            res = jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])
            self.logged_in = True
            return res
        except (jwt.DecodeError,jwt.ExpiredSignatureError) as e:
            print('!!',e)
            self.logged_in=False
            return False

    def handle_login(self, data:dict):
        with logmap('logging in') as lm:
            username = data.get('username','')
            password = data.get('password','')
            user = None
            try:
                user = User.login(name=username, password=password)
            except UserNotExist:
                try:
                    user = User.register(name=username, password=password)
                except Exception as e:
                    self.error = str(e)
                    self.logged_in=False
                    lm.error(e)
            except Exception as e:
                self.error = str(e)
                self.logged_in=False
                lm.error(e)
                
            
            if user:
                self.username = user.name
                self.logged_in=True
                self.error=''
                
                ## get payload
                # Current time
                now = datetime.utcnow()
                # Expiration time (e.g., 24 hours from now)
                exp_time = now + timedelta(hours=24)
                # Payload with an expiration claim
                payload = {
                    'sub': user.id,  # Subject (who the token is about)
                    'iat': now,  # Issued at: time when the JWT was issued
                    'exp': exp_time  # Expiration time
                }
                self.token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                self.store_opts(
                    username=self.username,
                    token=self.token
                )

    def store_opts(self, **opts):
        self.json = to_json({
            **from_json(self.json), 
            **opts,
        })

        
    def handle_logout(self):
        self.username=''
        self.token=''
        self.logged_in=False
        self.store_opts(username='',token='')

    def handle_post(self, data):
        payload = self.login_from_token()
        if payload:
            user = User.get(id=payload['sub'])
            post = data.get('post','')
            user.post(
                txt=post, 
                lat=self.lat,
                lon=self.lon, 
            )