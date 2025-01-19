import asyncio
import time
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

storage = {"stored_data": []}


# Request model for POST endpoints
class Data(BaseModel):
    value: str


@app.get("/")
async def root():
    return {"message": "Hello, from FastAPI :)"}


@app.get("/about")
async def about():
    """Retrieve stored data or suggest using the /save endpoint"""

    if storage["stored_data"]:
        return {
            "message": "Stored data retrieved successfully",
            "data": storage["stored_data"]
        }

    return {
        "message": "To store data on the server, hit the /save POST endpoint",
        "data": []
    }


@app.post("/process")
async def process(data: Data):
    """Process the value from the request body"""
    if not data.value.strip():
        raise HTTPException(status_code=400, detail="You must specify a value!")

    ###
    start_time = datetime.now().strftime('%H:%M:%S')
    print(f"Start processing at: {start_time}")
    
    await asyncio.sleep(5)  # simulate async delay/workload
    # time.sleep(5)  # synchronous blocking delay

    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"End processing at: {end_time}")
    ###

    return {"received_value": data.value}


@app.post("/save")
async def save(data: Data):
    """Save the value with a timestamp"""
    if not data.value.strip():
        raise HTTPException(status_code=400, detail="You must specify a value!")

    current_time = datetime.now().strftime('%H:%M:%S')
    storage["stored_data"].append({current_time: data.value})

    return {"message": f"{data.value} saved successfully!"}
