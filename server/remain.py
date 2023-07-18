from fastapi import Depends, FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    AWS_ACCESS_KEY: str
    

    class Config:
        env_file = '.env'


def get_settings():
    return Settings()


app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: str, settings: Settings = Depends(get_settings)):
    
    return {"SUPABASE_URL": settings.SUPABASE_URL, "item_id": item_id}