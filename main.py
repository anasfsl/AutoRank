import pandas as pd
import numpy as np
import requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Data Model 
class UserPreferences(BaseModel):
    make: str
    w_price: float
    w_mpg: float
    w_hp: float

# Live API & Simulation
def fetch_cars(make: str):
    # Live NHTSA API Call
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json"
    response = requests.get(url)
    data = response.json()
    
    # Process results into a Pandas DataFrame
    results = []
    
    # Limit to 10 cars for performance/demo
    models = data.get("Results", [])[:10]
    
    for item in models:
        # Simulate specs 
        results.append({
            "make": item["Make_Name"],
            "model": item["Model_Name"],
            "price": random.randint(20000, 60000),
            "mpg": random.randint(18, 55),
            "hp": random.randint(140, 400)
        })
    
    return pd.DataFrame(results)

# The Algorithm 
def calculate_topsis(df, weights):
    # weights = [w_price, w_mpg, w_hp]
    
    if df.empty:
        return df
    
    # Normalize the Matrix
    # Square each element, sum them, take square root
    norm_df = df[["price", "mpg", "hp"]].copy()
    
    # Price is a COST (lower is better), MPG/HP are BENEFITS (higher is better)
    # This is handled in the distance calculation step.
    
    for col in ["price", "mpg", "hp"]:
        norm_df[col] = df[col] / np.sqrt((df[col]**2).sum())
        
    # Apply Weights
    norm_df["price"] *= weights[0]
    norm_df["mpg"]   *= weights[1]
    norm_df["hp"]    *= weights[2]
    
    # Determine Ideal Best (V+) and Ideal Worst (V-)
    # For Price (Cost): Best is Min, Worst is Max
    # For MPG/HP (Benefit): Best is Max, Worst is Min
    best_ideal = [norm_df["price"].min(), norm_df["mpg"].max(), norm_df["hp"].max()]
    worst_ideal = [norm_df["price"].max(), norm_df["mpg"].min(), norm_df["hp"].min()]
    
    # Calculate Euclidean Distance to Ideal Best (S+) and Worst (S-)
    s_plus = np.sqrt(((norm_df[["price", "mpg", "hp"]] - best_ideal)**2).sum(axis=1))
    s_minus = np.sqrt(((norm_df[["price", "mpg", "hp"]] - worst_ideal)**2).sum(axis=1))
    
    # Calculate Performance Score
    # Score = S- / (S+ + S-)
    df["score"] = s_minus / (s_plus + s_minus)
    
    return df.sort_values(by="score", ascending=False)

# 4. Routes 
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/rank")
async def rank_cars(prefs: UserPreferences):
    # Fetch
    df = fetch_cars(prefs.make)
    
    if df.empty:
        return []

    # Algorithm
    # Convert 1-10 slider inputs to relative weights
    weights = [prefs.w_price, prefs.w_mpg, prefs.w_hp]
    ranked_df = calculate_topsis(df, weights)
    
    # Return JSON
    return ranked_df.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)