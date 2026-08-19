from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import os

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")

YC_API_KEY = os.environ["YC_API_KEY"]
YC_FOLDER_ID = os.environ["YC_FOLDER_ID"]

client = OpenAI(
    base_url="https://llm.api.cloud.yandex.net/v1",
    api_key="DUMMY",  # не используется, если переопределим заголовок
    default_headers={
        "Authorization": f"Api-Key {YC_API_KEY}",
        "OpenAI-Project": YC_FOLDER_ID,   # важно для совместимости
    },
)

print(client.models.list())
