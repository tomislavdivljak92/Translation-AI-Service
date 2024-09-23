import openai
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import load_dotenv
import os

# Load environment variables and OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    translations = {}
    for lang in languages:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Ensure the correct model is used
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant that translates text into {lang}."},
                    {"role": "user", "content": text}
                ],
                max_tokens=1000
            )
            translated_text = response['choices'][0]['message']['content'].strip()
            translations[lang] = translated_text
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            translations[lang] = f"Error: {e}"

    # Pass task_id directly, since it is already an integer
    update_translation_task(db, task_id, translations)

# Test model list retrieval to verify models are available
#models = openai.Model.list()
#print(models)