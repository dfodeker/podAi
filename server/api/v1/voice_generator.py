import requests

class ElevenLabsService:
    def __init__(self, xi_api_key: str, url: str):
        self.xi_api_key = xi_api_key
        self.url = url

    def text_to_speech(self, text: str, model_id: str = "eleven_monolingual_v1") -> str:
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.xi_api_key
        }
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(self.url, json=data, headers=headers)
        audio_file_path = 'ceader.mp3'
        with open(audio_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return audio_file_path
