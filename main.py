from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import requests
import json
from system_prompt import business_agent_system_prompt

load_dotenv()

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

"""
The requirements to build basic galileonix are
 Understanding the Business Problem
 Data Collection
 Data Cleaning / Preprocessing
 Data Exploration (EDA : Exploratory Data Analysis)
 Data Visualization
 Deriving Insights and Recommendations
 Reporting
"""


@app.get("/")
def root():
    return {"message": "Welcome to DAK, this is Trixy"}


class Problem(BaseModel):
    statement: str

@app.post("/business-problem")
def business_problem(problem: Problem):
    request = problem.statement

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[
            {
                "role": "system",
                "content":business_agent_system_prompt,
            },
            {
                "role":"user",
                "content":request
            }
        ]
    )

    return {
        "message": "Problem statement analysed successfully",
        "solution":completion
    }

class Collection(BaseModel):
    api_endpoint:str

@app.post("/data-collection")
def data_collection(api:Collection):
    # collect data from multiple source
    # api basic hit to any endpoint
    response = requests.get(api.api_endpoint)
    return response.text
    # connect to sql db's

    # then put these together in a unfied source that is csv
    


@app.post("/data-cleaning")
def data_cleaning():
    # clean data using autoclean or i'll write a simple custom script
    # first provide insights then use autoclean to clean the data
    # return the final file
    pass


@app.post("/data-viz")
def data_viz():
    # get the info from the dataset
    # then return the stats
    # we'll viz on the frontend
    pass


@app.post("/assistant")
def analytics():
    # upload csv
    # write a feedback engine
    # build analytics
    pass


@app.post("/reporter")
def reporter():
    # csv -> get stats -> report
    # connect to db run queries basic sql one's via ai
    # get a detailed report
    pass
