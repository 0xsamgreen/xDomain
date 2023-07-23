import pickle
from datetime import datetime
from typing import Any, Dict, List
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
from collections import defaultdict
import pandas as pd
from typing import Dict

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5001",  # React application's address
    "http://localhost:5000",
    "http://localhost:8000",  # React application's address
    "http://localhost:8100",  # React application's address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def convertStringToList(path):
    return [int(float(k)) for k in path[1:-1].split(",")]


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
    global opps_metadata_df

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

    opps_metadata_df = pd.read_csv("assets/opps_metadata-2023-3-19.csv").reset_index(
        drop=True
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


class BarDataSeize(BaseModel):
    date: str
    amount: float


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


class CurrentOppSeize(BaseModel):
    token: str
    amount: float


# returns mockOpportunities
@app.get("/current_opp", response_model=List[CurrentOppSeize])
def current_opp():
    try:
        url = "https://odos.xyz/api/latest-arbs"

        response = requests.get(url)

        # Checking the status code, 200 means the request was successful
        if response.status_code == 200:
            odos_data = response.json()
            best_opportunities = odos_data["best_paths"]
        else:
            print("Error:", response.status_code)

        # Extract the token name and amount from the best opportunities
        results = []
        for i in range(10):
            opportunity_details = {}
            path = best_opportunities[i]
            opportunity_details["token"] = path["path"][0]["token_in_symbol"]
            opportunity_details["amount"] = path["profitUSD"]
            results.append(opportunity_details)
        return results
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class MockFrequencySeize(BaseModel):
    frequency: int
    amount: float


# returns mockFrequency
@app.get("/opp_frequency", response_model=List[MockFrequencySeize])
async def opp_frequency(n_bins: int = 100):
    global unique_opps_profit_time
    all_opp_cluster_min = []
    for key, metadata in unique_opps_profit_time.items():
        profits = metadata["profits"]
        if len(profits) == 0:
            continue
        all_opp_cluster_min += min(profits)
    hist, bin_edges = np.histogram(
        all_opp_cluster_min, range=[0, max(all_opp_cluster_min)], bins=n_bins
    )

    # preparing data in a required format
    data = []
    for frequency, amount in zip(hist.tolist(), bin_edges.tolist()):
        if frequency != 0:
            data.append({"frequency": frequency, "amount": amount})

    return data


@app.get("/token_totals_paths", response_class=JSONResponse)
async def token_totals_paths():
    global opps_metadata_df

    # Initialize the defaultdict with int as the default factory
    token_profits = {}

    # First assign all the keys to token_profits. Each key is a unique token
    for path, metadata in unique_opps_profit_time.items():
        # Get the token that the path starts with
        path = convertStringToList(path)

        path_tokens_list = []
        for swap_id in path:
            if swap_id == 0:
                continue
            token = opps_metadata_df[opps_metadata_df["swap_id"] == swap_id][
                "token_in_symbol"
            ].iloc[0]
            path_tokens_list.append(token)

        path_tokens_string = "_".join(path_tokens_list)
        input_token = path_tokens_list[0]
        # Needs to start and end with same token
        path_tokens_string += f"_{input_token}"

        # Track unique tokens
        if input_token not in token_profits.keys():
            token_profits[input_token] = {"token": input_token}

        for profit_cluster in metadata["profits"]:
            if path_tokens_string not in token_profits[input_token].keys():
                token_profits[input_token][path_tokens_string] = 0.0
            token_profits[input_token][path_tokens_string] += min(profit_cluster)

    # Sort the inner dictionary based on values
    for key in token_profits.keys():
        # Exclude the 'token' key
        items = [(k, v) for k, v in token_profits[key].items() if k != "token"]
        sorted_items = dict(sorted(items, key=lambda x: x[1], reverse=True))

        # Add 'token' key back to the start of the sorted dictionary
        token_profits[key] = {"token": token_profits[key]["token"], **sorted_items}

    # Convert the defaultdict to a list of dictionaries
    data = [token_dict for token_dict in token_profits.values()]

    return data


@app.get("/token_paths", response_class=JSONResponse)
async def token_paths():
    global opps_metadata_df
    all_token_paths = []
    # First assign all the keys to token_profits. Each key is a unique token
    for path, metadata in unique_opps_profit_time.items():
        # Get the token that the path starts with
        path = convertStringToList(path)

        path_tokens_list = []
        for swap_id in path:
            if swap_id == 0:
                continue
            token = opps_metadata_df[opps_metadata_df["swap_id"] == swap_id][
                "token_in_symbol"
            ].iloc[0]
            path_tokens_list.append(token)

        path_tokens_string = "_".join(path_tokens_list)
        input_token = path_tokens_list[0]
        # Needs to start and end with same token
        path_tokens_string += f"_{input_token}"

        if path_tokens_string not in all_token_paths:
            all_token_paths.append(path_tokens_string)

    return all_token_paths


@app.get("/latency_histogram", response_class=JSONResponse)
async def latency_histogram():
    durations = []
    for key, metadata in unique_opps_profit_time.items():
        durations.append(metadata["opportunity_duration_sum"])

    n_bins = 500
    hist, bin_edges = np.histogram(durations, range=[0, 500], bins=n_bins)
    print(hist)
    print(bin_edges)
    # preparing data in a required format
    data = [
        {"time": time, "amount": amount}
        for amount, time in zip(hist.tolist(), bin_edges.tolist())
    ]

    return data


@app.get("/total_opportunity", response_class=JSONResponse)
async def total_opp():
    min_profit_sum = 0
    for key, metadata in unique_opps_profit_time.items():
        min_profit_sum += unique_opps_profit_time[key]["min_profit_sum"]
    return min_profit_sum
