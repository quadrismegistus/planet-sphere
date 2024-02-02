from ..imports import *

class UserState(rx.State):
    json: dict = rx.LocalStorage('{}')
    username: str = ''

    def init(self):
        data=from_json(self.json)
        self.username=data.get('username','')

    def handle_login(self, data:dict):
        print(data)
        self.username = data.get('username','')
        self.json = to_json({**from_json(self.json), **data})