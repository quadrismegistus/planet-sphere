from flatearth import *
from pydantic import BaseModel
from typing import List
from datetime import timedelta
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Secret key for JWT encoding and decoding
SECRET_KEY = "alltheworldaflatcircle"
ALGORITHM = "HS256"

# Define a list of allowed origins for CORS
# You can use "*" to allow all origins or specify only the ones you need
origins = [
    "http://localhost:8100",  # Assuming your React app runs on this port
    "http://localhost:3000",  # Commonly used port for React development
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
    return df[['id','lat','lon','content']].to_dict('records')


@app.get("/posts/latest")
async def get_posts():
    """
    Endpoint to receive latitude and longitude as path parameters and return them.
    """
    df = post_map_df().rename(columns={'html':'content'})
    return df[['id','lat','lon','content']].sort_values(['lon','lat']).to_dict('records')





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
        
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": query.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "msg":"OK"}
    except UserError as e:
        return {"status":400, 'msg':str(e)}
    

    



class PlaceQuery(BaseModel):
    lat: float
    lon: float

@app.post("/places/query")
async def get_place(query:PlaceQuery):
    """
    Endpoint to receive latitude and longitude as path parameters and return them.
    """
    place = Place.locate(lat=query.lat, lon=query.lon)
    return place.data if place else {}










# Generate JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default to 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
