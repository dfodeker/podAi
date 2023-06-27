from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse
import openai
import os
import requests
import boto3

openai.api_key = ""
xi_api_key = ""
url = "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>"

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None



@app.get("/")
async def read_root():
    return {"Hello": "World"}
   


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



@app.post("/ask2")
async def ask2(question: str):
   conversation = [
    {"role": "system", "content": "You are a helpful and knowledgeable podcast co-host with a good sense of humor. You enjoy dropping pop culture references, telling funny stories, and using slightly obscure metaphors. You're always charming, upbeat, and keen on avoiding information overload."},
    {"role": "user", "content": question},
]
   response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=conversation,
        max_tokens=10
    )
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
    audio_file_path = 'output.mp3'
    with open(audio_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
        uploadAudio(audio_file_path) 
        return {"James said": speak, "file_path": audio_file_path}
   
def uploadAudio(file_path: str):
    counter = 1 
    session = boto3.Session(
         aws_access_key_id = '',
         aws_secret_access_key = ''
        )
    s3 = session.client('s3', endpoint_url='')

    bucket_name = 'ai-bucket'  # Replace with your bucket name
    object_key = f'output{counter}.mp3'
    s3.upload_file(file_path, bucket_name, object_key)
    counter += 1
    print("Upload Successful")



