from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import requests
import json
from system_prompt import business_agent_system_prompt
import psycopg2
from AutoClean import AutoClean
import pandas as pd

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
    # return response.text
    # connect to sql db's
    DB_STRING=os.getenv("DB_STRING")
    conn=psycopg2.connect(DB_STRING)
    print("Connection to PostgreSQL successful!")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;") # just a sample we change according to our needs
    rows = cur.fetchall()
    print("Data from 'users' table:")
    for row in rows:
        row = row
    return (
        response.text,
        row
    )

@app.get("/data-cleaning")
def data_cleaning():
    # clean data using autoclean or i'll write a simple custom script
    # first provide insights then use autoclean to clean the data
    # return the final file
    try:
        df = pd.read_csv("messy_data.csv")
        pipeline = AutoClean(df)
        pipeline.output.to_csv("output.csv", index=False)
        print("cleaned successfully")
    except Exception as e:
        print("error:", e)


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
