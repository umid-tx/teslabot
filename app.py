from transformers import pipeline
from fastapi import FastAPI
from mangum import Mangum

from pydantic import BaseModel  # Enforces the type, getting the benefit of static typing.
from typing import List

#  dynamically-typed languages perform type checking at runtime, while statically typed languages perform type checking at compile time.

class BodyModel(BaseModel):
    comments: List[str] 
   


model_path = 'model'
classify = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)

app = FastAPI(title='Serverless Lambda FastAPI', root_path="/Prod/")  # root path is the proxy


@app.post("/sentiment", tags=["Sentiment Analysis"])  # to create data
def sentiment( item: BodyModel):
    comments = item.comments
    return {'result': classify(comments)}



@app.get("/", tags=["Health Check"])  # checking health of the server 
def root():
    return {"message": "Ok"}


handler = Mangum(app=app)  # It is a configurable wrapper that allows any ASGI (Asynchronous Server Gateway Interface) application (or framework) to run in an AWS Lambda deployment.

### The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:
##### - the path /
##### - using a get operation

### That @something syntax in Python is called a "decorator". A "decorator" takes the function below and does something with it.