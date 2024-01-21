from tqdm import tqdm
import random
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import Lock
import random
from datetime import datetime, timedelta
import base64
import os
import json
from pathlib import Path
from urllib.parse import urlparse
import time
import requests
from quart import Quart, g, jsonify, request, Response, abort, stream_with_context
from quart_cors import cors
import tempfile
import yaml
import uuid
from quart import current_app
from dotenv import load_dotenv
from openai import AzureOpenAI
from newsapi import NewsApiClient

from firebase_admin.firestore import Query
from firebase_admin import auth, messaging
from firebase_admin import credentials, firestore, initialize_app

load_dotenv()


def generateQuestion():

    newsApi = NewsApiClient(api_key="ad0df79148454c949b6b6f0f51adaadc")
    azure_gpt35_model = AzureOpenAI(
        azure_endpoint="https://cerebrus-openai-prod-northus.openai.azure.com/",
        api_key="3f8729d687644797893788a59bc3e8e7",
        api_version="2023-07-01-preview",
    )
    category = random.choice(["business", "entertainment",
                              "general", "health", "science", "sports", "technology"])
    question_type = random.choice(["controversial", "would you rather", ""])
    headlines = newsApi.get_top_headlines(country="us", category=category)
    headline = random.choice(headlines["articles"])["title"]

    if (question_type == ""):
        topic = headline + ". Give a quick background knowledge on the topic."
    else:
        topic = "a well known or interesting topic"

    response = azure_gpt35_model.chat.completions.create(
        model="spooky-main",
        messages=[
            {
                "role": "system",
                "content": "You are a young ponderous individual who loves to ask" + question_type + "questions. You do not ask too formally. You are not too involved with politics."
            },
            {
                "role": "user",
                "content": "Generate a short question that sparks debate or discussion about " + topic + ". It should not be a yes or no question."
            }
        ],
    )
    return [response.choices[0].message.content, uuid.uuid4()]


def proxy_post(url, data):
    return requests.post(url, json=data)


app = Quart(__name__)
# Allow localhost:3000 to not get CORS errors
app = cors(app, allow_origin="*")

with open("config/config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

cred = credentials.Certificate(
    "config/firebase.json")

default_app = initialize_app(cred)
db = firestore.client()

# your colletcions here
QUESTIONS = db.collection("questions")
USERS = db.collection("users")
# COMMUNICATIONS = db.collection("Communications")
# AGENTS = db.collection("Agents")
# FEEDBACK = db.collection("Feedback")
