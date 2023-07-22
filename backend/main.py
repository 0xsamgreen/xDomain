from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import numpy as np
import pandas as pd
from datetime import datetime
import pickle

app = FastAPI()


def timestamp_to_date(timestamp):
    # Convert the timestamp (seconds since the epoch) to a datetime object
    dt_object = datetime.fromtimestamp(timestamp)

    # Format the datetime object as a string in the desired format
    date_string = dt_object.strftime("%-d %b %y")

    return date_string


# For a given timestamp range, return the total opportunity
def total_opp_in_range(timestamp_start, timestamp_end):
    global unique_opps_profit_time
    opportunity_sum = 0
    for key, metadata in unique_opps_profit_time.items():
        for timestamps, profits in zip(metadata["timestamps"], metadata["profits"]):
            if timestamps[0] < timestamp_start or timestamps[-1] > timestamp_end:
                continue
            opportunity_sum += min(profits)
    return opportunity_sum


@app.on_event("startup")
async def load_dataframes():
    global opps_df
    global opps_metadata_df
    global path_data
    global unique_opps_profit_time
    global unique_paths
    global unique_timestamps
    global block_rate
    global stats

    print("Loading variables from .pkl files...")
    with open("assets/opps.pkl", "rb") as f:
        opps_df = pickle.load(f)

    with open("assets/opps_metadata_df.pkl", "rb") as f:
        opps_metadata_df = pickle.load(f)

    with open("assets/path_data.pkl", "rb") as f:
        path_data = pickle.load(f)

    with open("assets/unique_opps_profit_time.pkl", "rb") as f:
        unique_opps_profit_time = pickle.load(f)

    with open("assets/unique_paths.pkl", "rb") as f:
        unique_paths = pickle.load(f)

    with open("assets/unique_timestamps.pkl", "rb") as f:
        unique_timestamps = pickle.load(f)

    with open("assets/block_rate.pkl", "rb") as f:
        block_rate = pickle.load(f)

    with open("assets/stats.pkl", "rb") as f:
        stats = pickle.load(f)
    print("Finished loading variables from .pkl files...")


@app.get("/")
def read_root():
    return {"Hello": "World"}


class BarDataSeize(BaseModel):
    date: str
    amount: float


class PlotRequest(BaseModel):
    from_date: str
    to_date: str


# returns mockBarDataSize
@app.get("/data_daily_opp", response_model=List[BarDataSeize])
def data_daily_opp(epoch_start: int):
    try:
        epoch_start = int(epoch_start)
        daily_total_opp = []
        # Starting with `epoch_start`, get the daily opp. total for the next 30 days.
        for i in range(1, 31):
            epoch_day_start = epoch_start + 86400 * (i - 1)
            epoch_day_end = epoch_start + 86400 * i
            opportunity_sum = total_opp_in_range(epoch_day_start, epoch_day_end)

            daily_total_opp.append(
                {
                    "date": timestamp_to_date(epoch_day_start),
                    "amount": opportunity_sum,
                }
            )
        print(f"daily_total_opp: {daily_total_opp}")
        return daily_total_opp
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
