# podAi

This is a Python project that utilizes the FastAPI framework to create a web application with several endpoints. The app provides functionalities to retrieve and update item information, as well as ask questions and generate responses using OpenAI's language models. Additionally, the app includes text-to-speech capabilities and the ability to upload audio files to an Amazon S3 bucket. (Under active development)




### Prerequisites
- Python 3.x
- FastAPI
- OpenAI Python library
- xi-api-key (Eleven Labs API key)
- AWS credentials (access key and secret access key) with S3 permissions

### Setup

1. Clone the repository or download the source code files.

2. Install the required dependencies by running the following command:
   ```
   pip install fastapi openai boto3 requests
   ```

3. Replace the `xi_api_key` and AWS credentials (`aws_access_key_id` and `aws_secret_access_key`) with the respective values in the `textToSpeech` function.

4. Update the `url` variable in the `textToSpeech` function with the appropriate Eleven Labs API endpoint.

5. Replace the `endpoint_url` variable in the `uploadAudio` function with the appropriate AWS S3 endpoint URL.

6. Modify the `bucket_name` variable in the `uploadAudio` function to match the name of your desired S3 bucket.

### Usage

To start the application, run the following command in your terminal:
```
uvicorn main:app --reload
```

The application will be accessible at `http://localhost:8000`.

#### Endpoints

1. `GET /`
   - Returns a JSON response with the message: {"Hello": "World"}.

2. `GET /items/{item_id}`
   - Retrieves item information based on the provided `item_id` path parameter and an optional query parameter `q`.
   - Returns a JSON response with the `item_id` and `q` values.

3. `PUT /items/{item_id}`
   - Updates an item based on the provided `item_id` path parameter and the request body containing an `Item` object.
   - Returns a JSON response with the updated `item_name` and `item_id`.

4. `POST /ask`
   - Accepts a question in the request body and generates a response using OpenAI's text-davinci-002 engine.
   - Returns a JSON response with the generated response from OpenAI.

5. `POST /ask2`
   - Accepts a question in the request body and generates a response using OpenAI's gpt-3.5-turbo-16k model.
   - Converts the generated response to speech using text-to-speech capabilities and saves the audio file.
   - Uploads the audio file to an Amazon S3 bucket.
   - Returns a JSON response with the generated response and the file path of the uploaded audio file.
6. `POST /transcribe`   
   - Accepts an audio file, transcribes it, and generates a response based on the transcribed text.



## Features in Development

- **Similarity Detection**: Uses NLP techniques such as Semantic Similarity with Transformer models, TF-IDF, and Siamese Networks to search through past interactions for input similar to the current user input.
- **Topic Extraction**: Incorporates topic modeling techniques such as LDA, NMF, and BERTopic to determine the main theme of the conversation from similar past interactions.
- **Emotion in Voice Synthesis**: Utilizes advanced speech synthesis technologies and prosody modification to create voices with depth and emotion, aspiring to match the quality of systems like Sonantic.



### Acknowledgments

This project utilizes the FastAPI framework and OpenAI's language models to provide a web application with advanced language processing capabilities. The text-to-speech functionality is powered by the Eleven Labs API, and the audio file uploads are facilitated by Amazon S3.

### Thoughts
 
Considering using whisper-x for transcriptions to reduce the number of API calls to OpenAI.
thinking about ways to improve the conversation flow and make it more natural by remembering previous interactions