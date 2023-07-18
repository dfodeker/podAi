import tempfile
from datetime import datetime, timedelta
from typing import Union
from httpx import HTTPStatusError
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import openai
import os
from typing import Annotated
import requests
import boto3
from supabase import create_client, Client
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from jose import jwt
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings



from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    SUPABASE_URL: str
    AWS_ACCESS_KEY: str
    OPENAI_KEY: str
    S3_BUCKET: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    URL: str
    SECRET_KEY: str
    
    class Config:
        env_file = '.env'
   
def get_settings():
    return Settings()

SupaUrl = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SupaUrl, key)
url= os.environ.get('URL')
openai.api_key = os.environ.get('OPENAI_KEY')
xi_api_key = os.environ.get('XI_API_KEY')
s3_endpoint = os.environ.get('S3_BUCKET')
aws_access_key = os.environ.get('AWS_ACCESS_KEY')
aws_secret_key = os.environ.get('AWS_SECRET_KEY')

SECRET_KEY="d8e2d3dfd513073e0e5f4a45c964cbefb60a706faae95cb33304a00d3d627570"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class Interaction(BaseModel):
    user_id: str
    user_input: str


app = FastAPI()
supabase: Client = create_client(SupaUrl, key)

origins = [
    "http://localhost:3000",  # React app address
    "http://localhost.tiangolo.com",
    "http://your-react-app-url-or-ip", # if it's deployed
    "http://your-fastapi-app-url-or-ip", # your fastapi app url or ip
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/sign_in")
async def sign_in(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        if 'error' in response:
            # Log the error message for debugging purposes
            print(f"Sign in error: {response['error'].get('message')}")
            
            # Raise an HTTPException to return a 401 Unauthorized response
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return response.session.access_token
    except HTTPStatusError as error:
        if error.response.status_code == 400:
            # Log the error message for debugging purposes
            print(f"HTTPStatusError: {error}")
            
            # Raise an HTTPException to return a 400 Bad Request response
            raise HTTPException(
                status_code=400,
                detail="Bad request",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            # If it's not a 400 error, re-raise the exception
            raise

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.post("/interact")
async def interact(interaction: Interaction):
    # Get the last interaction from this user.
    
    past_interactions = supabase.table('interactions').select('user_id','user_input').execute()
    
    #we need an algo to search through interactions for similar user input similar denoting a high probability of same topic
    #if similar is found we use the similarity to determine "main theme" of the conversation and use that to determine the prompt
    #if no similar is found we craft a completely new prompt
    #we then use the prompt to generate a response

    # Prepare the prompt for GPT-4.
    
    return {'prompt': past_interactions,}

@app.get("/")
async def read_root(settings: Settings = Depends(get_settings)):
    print(settings.SUPABASE_URL)
    return{"SUPABASE_URL": settings.SUPABASE_URL}
   
  # Initialize your ASR handler

@app.get("/transcribe")
async def transcribe(file_path: str):
    return {"file_path": file_path}



@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


   

@app.post("/ask")
async def ask(question: str):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=10
    )

    return {"James said": response.choices[0].text.strip()}


@app.post("/transcribe")
async def create_upload_file(file: UploadFile):
    contents = await file.read()

    # Save the file
    with open(file.filename, "wb") as f:
        f.write(contents)

    # Now that the file is saved, read it back and pass it to the transcribe function
    with open(file.filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    #response = await ask2(transcript)
    transcript_text = transcript['text']

    response = await ask2(transcript_text)

    return {"filename": file.filename, "transcript": transcript_text, "response": response}


@app.post("/ask2")
async def ask2(question: str):
   conversation = [
    {"role": "system", "content": "You are a helpful and knowledgeable podcast co-host with a good sense of humor. You enjoy dropping pop culture references, telling funny stories, and using slightly obscure metaphors. You're always charming, upbeat, and keen on avoiding information overload.You are an engaging and friendly AI with extensive knowledge in various topics. You enjoy making conversations interesting with a touch of humor and personal anecdotes, when appropriate. You're always respectful, patient, and strive to provide detailed and helpful responses. You aim to make the interaction as human-like as possible, offering thoughtful insights and asking follow-up questions."},
    {"role": "user", "content": question},
]
   response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=conversation,
        temperature=1.24,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0.19,
        presence_penalty=0
    )
   print(response)
   speak = response.choices[0].message['content'].strip()
   print(speak)
   textToSpeech(speak)

   return {"James said": speak}


def textToSpeech(speak: str):
    headers = {
        "Accept": "audio/mpeg",
         "Content-Type": "application/json",
        "xi-api-key": xi_api_key
    }
    data = {
        "text": speak,  # replace with AI response
        "model_id": "eleven_monolingual_v1",  # you may need to change this to the specific model_id you're using
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
            }
        }

# Send a POST request to the Eleven Labs API
    response = requests.post(url, json=data, headers=headers)

# Save the returned audio to an mp3 file\
    audio_file_path = 'ceader.mp3'
    with open(audio_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
        uploadAudio(audio_file_path) 
        return {"James said": speak, "file_path": audio_file_path}
   
def uploadAudio(file_path: str):
    counter = 1 
    session = boto3.Session(
         aws_access_key_id = aws_access_key,
         aws_secret_access_key = aws_secret_key
        )
    s3 = session.client('s3', endpoint_url=s3_endpoint)

    bucket_name = 'ai-bucket'  # Replace with your bucket name
    object_key = f'output{counter}.mp3'
    s3.upload_file(file_path, bucket_name, object_key)
    counter += 1
    print("Upload Successful")



