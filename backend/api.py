from flatearth import *
from pydantic import BaseModel
from typing import List
from datetime import timedelta
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException, status

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins - for testing only!
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Secret key for JWT encoding and decoding
SECRET_KEY = "alltheworldaflatcircle"
ALGORITHM = "HS256"

# Define a list of allowed origins for CORS
# You can use "*" to allow all origins or specify only the ones you need
origins = [
    "*"
    # "http://localhost:8100",  # Assuming your React app runs on this port
    # "http://localhost:3000",  # Commonly used port for React development
    # Add any other origins you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class PostQuery(BaseModel):
    type: str
    seen: List[int]

@app.post("/posts/query")
async def get_posts(query:PostQuery):
    """
    Endpoint to receive latitude and longitude as path parameters and return them.
    """
    logger.debug(query)
    df = post_map_df(seen=query.seen).rename(columns={'html':'content'})
    return df[['id','lat','lon','content','size']].sample(frac=1).to_dict('records')


@app.get("/posts/latest")
async def get_posts():
    """
    Endpoint to receive latitude and longitude as path parameters and return them.
    """
    df = post_map_df().rename(columns={'html':'content'})
    
    return df[['id','lat','lon','content','size']].sample(frac=1).to_dict('records')





class LoginQuery(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(query:LoginQuery):
    try:
        try:
            user = User.login(name=query.username, password=query.password)
        except UserNotExist:
            user = User.register(name=query.username, password=query.password)
        
        access_token = create_access_token(query.username)
        return {"access_token": access_token, "token_type": "bearer", "msg":"OK"}
    except UserError as e:
        return {"status":400, 'msg':str(e)}

    



class PlaceQuery(BaseModel):
    geonames_id:int

@app.get("/places/query")
async def get_place(geonames_id:int):
    """
    Endpoint to receive latitude and longitude as path parameters and return them.
    """
    place = Place.from_geonames(geonames_id)
    return place.data if place else {}





class PostQuery(BaseModel):
    access_token: str
    post_txt: str
    geonames_id: int

@app.post("/login")
async def make_post(query:PostQuery):
    username = verify_access_token(query.access_token)
    user = User.get(name=username)
    post = user.post(query.post_txt, geonames_id=query.geonames_id)
    return post.data






# Generate JWT token
def create_access_token(username:str):
    expires_delta = timedelta(minutes=30)
    to_encode={"sub": username, 'exp':datetime.utcnow() + expires_delta}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # Extracting the username
        if username is None:
            raise credentials_exception
        return username  # Now returning the username instead of the whole payload
    except jwt.PyJWTError:
        raise credentials_exception