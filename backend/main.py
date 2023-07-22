from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import numpy as np
import pandas as pd

app = FastAPI()


class PlotRequest(BaseModel):
    from_date: str
    to_date: str


@app.on_event("startup")
async def load_dataframes():
    global opps_df
    global opps_metadata_df
    global path_data

    print("Loading path data...")
    opps_df = pd.read_csv("opps_cleaned-2023-3-19.csv").reset_index(drop=True)
    opps_metadata_df = pd.read_csv("opps_metadata-2023-3-19.csv").reset_index(drop=True)
    print("Finished loading path data!")

    print("Searching for unique paths in `opps_df` archive...")

    unique_paths = opps_df[
        ["swap_1_id", "swap_2_id", "swap_3_id", "swap_4_id"]
    ].drop_duplicates()
    unique_paths.reset_index(inplace=True)
    print(unique_paths)


@app.get("/")
def read_root():
    return {"Hello": "World"}


class BarDataSeize(BaseModel):
    date: str
    amount: int
    amountColor: str


@app.get("/data_daily_opp", response_model=List[BarDataSeize])
def data_daily_opp():
    return [
        {
            "date": "5 Jan 23",
            "amount": 100,
            "amountColor": "hsl(229, 70%, 50%)",
        },
        {
            "date": "6 Jan 23",
            "amount": 10000,
            "amountColor": "hsl(229, 70%, 50%)",
        },
    ]
