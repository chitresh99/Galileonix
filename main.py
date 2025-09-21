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
import numpy as np

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
        return {"message":"Data cleaned successfully"}
    except Exception as e:
        print("error:", e)


@app.post("/data-viz")
def data_viz():
    # get the info from the dataset
    # then return the stats
    # we'll viz on the frontend
    pass

def clean_dict(d):
    """convert numpy types, NaN, inf into JSON-safe values"""
    if isinstance(d, dict):
        return {k: clean_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_dict(v) for v in d]
    elif pd.isna(d):
        return None
    elif isinstance(d, (np.int64, np.int32, np.int16)):
        return int(d)
    elif isinstance(d, (np.float64, np.float32, np.float16)):
        return float(d)
    return d

@app.get("/assistant")
def analytics():
    # upload csv
    # write a feedback engine
    # build analytics
    try:
        file_path = "messy_data.csv"
        df = pd.read_csv(file_path)

        report = {}

        # 1. basic info
        report["basic_info"] = {
            "shape": f"{df.shape[0]} rows × {df.shape[1]} columns",
            "file_size_kb": round(os.path.getsize(file_path) / 1024, 2)
        }

        # 2. column info
        report["columns"] = [
            {"index": i, "name": col, "dtype": str(df[col].dtype)}
            for i, col in enumerate(df.columns, 1)
        ]

        # 3. data types summary
        dtype_counts = df.dtypes.value_counts()
        report["data_types_summary"] = {
            str(dtype): int(count) for dtype, count in dtype_counts.items()
        }

        # 4. missing values
        missing = df.isnull().sum()
        missing_percent = (missing / len(df)) * 100
        missing_report = {
            col: {"count": int(missing[col]), "percent": round(missing_percent[col], 1)}
            for col in df.columns if missing[col] > 0
        }
        report["missing_values"] = (
            missing_report if missing_report else "no missing values found"
        )

        # 5. first 3 rows
        report["first_3_rows"] = clean_dict(df.head(3).to_dict(orient="records"))

        # 6. numeric columns summary
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            report["numeric_summary"] = clean_dict(
                df[numeric_cols].describe().round(2).to_dict()
            )

        # 7. categorical columns info
        categorical_cols = df.select_dtypes(include=['object']).columns
        categorical_info = {}
        for col in categorical_cols:
            unique_count = df[col].nunique()
            if unique_count <= 10:
                values = df[col].dropna().unique().tolist()
            else:
                values = df[col].value_counts().head(3).to_dict()
            categorical_info[col] = {
                "unique_count": int(unique_count),
                "values": clean_dict(values)
            }
        if categorical_info:
            report["categorical_columns"] = categorical_info

        # 8. potential issues
        issues = []
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            issues.append(f"duplicate rows: {duplicates}")
        for col in df.columns:
            if df[col].nunique() == 1:
                issues.append(f"column '{col}' has only one unique value")
            if missing_percent[col] > 50:
                issues.append(f"column '{col}' has >50% missing values")
        report["potential_issues"] = issues if issues else "no obvious issues detected"

        return clean_dict(report)

    except Exception as e:
        return {"error": str(e)}


@app.post("/reporter")
def reporter():
    # csv -> get stats -> report
    # connect to db run queries basic sql one's via ai
    # get a detailed report
    pass
