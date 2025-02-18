# Import libraries 
import json
import requests 
import pandas as pd
from typing import List

#Authentication for web scraping API

USERNAME = ""
PASSWORD = ""

# Build payload: COnfiguration for API on how to prcoess request 

query = "bicicleta"

print (f" Getting data from Google Trends for {query} keyword...")

# Google Trends URL ro eqfine the query and scrape the relevant data 
url = "https://realtime.oxylabs/v1/queries"
auth = (USERNAME, PASSWORD)

payload = {
    "source": "google_trends_explore"
    "query": query 
}

try: 
    response = requests.request("POST", url, auth = auth, json = payload)
except requests.exceptions.Request.Exception as e: 
    print ("Caught exception while getting trend data")

data = response.json()
content = data["results"][0]["content"]
print (content)


def flatten_topic_data(topics_data: List[dict]) -> List[dict]:
   """Flattens related_topic data"""
   topics_items = []
   for item in topics_data[0]["items"]:
       item_dict = {
           "mid": item["topic"]["mid"],
           "title": item["topic"]["title"],
           "type": item["topic"]["type"],
           "value": item["value"],
           "formatted_value": item["formatted_value"],
           "link": item["link"],
           "keyword": topics_data[0]["keyword"],
       }
       topics_items.append(item_dict)

   return topics_items

trend_data = json.loads(content)
print("Creating dataframes..")

   # Interest over time
iot_df = pd.DataFrame(trend_data["interest_over_time"][0]["items"])
iot_df["keyword"] = trend_data["interest_over_time"][0]["keyword"]

   # Breakdown by region
bbr_df = pd.DataFrame(trend_data["breakdown_by_region"][0]["items"])
bbr_df["keyword"] = trend_data["breakdown_by_region"][0]["keyword"]

   # Related topics
rt_data = flatten_topic_data(trend_data["related_topics"])
rt_df = pd.DataFrame(rt_data)

   # Related queries
rq_df = pd.DataFrame(trend_data["related_queries"][0]["items"])
rq_df["keyword"] = trend_data["related_queries"][0]["keyword"]     

CSV_FILE_DIR = "./csv/"

keyword = trend_data["interest_over_time"][0]["keyword"]
keyword_path = os.path.join(CSV_FILE_DIR, keyword)

try:
    os.makedirs(keyword_path, exist_ok=True)
except OSError as e:
    print("Caught exception while creating directories.")
    raise e

print("Dumping to CSV...")
iot_df.to_csv(f"{keyword_path}/interest_over_time.csv", index=False)
bbr_df.to_csv(f"{keyword_path}/breakdown_by_region.csv", index=False)
rt_df.to_csv(f"{keyword_path}/related_topics.csv", index=False)
rq_df.to_csv(f"{keyword_path}/related_queries.csv", index=False)

def get_trend_data(query: str) -> dict:
   """Gets a dictionary of trends based on given query string from Google Trends via Web Scraper API"""
   print(f"Getting data from Google Trends for {query} keyword..")
   url = "https://realtime.oxylabs.io/v1/queries"
   auth = (USERNAME, PASSWORD)
   payload = {
       "source": "google_trends_explore",
       "query": query,
   }
   try:
       response = requests.request("POST", url, auth=auth, json=payload)
   except requests.exceptions.RequestException as e:
       print("Caught exception while getting trend data")
       raise e

   data = response.json()
   content = data["results"][0]["content"]
   return json.loads(content)

def dump_trend_data_to_csv(trend_data: dict) -> dict:
   """Dumps given trend data to generated CSV file"""
   CSV_FILE_DIR = "./csv/"
   # Interest over time
   print("Creating dataframes..")
   iot_df = pd.DataFrame(trend_data["interest_over_time"][0]["items"])
   iot_df["keyword"] = trend_data["interest_over_time"][0]["keyword"]

   # Breakdown by region
   bbr_df = pd.DataFrame(trend_data["breakdown_by_region"][0]["items"])
   bbr_df["keyword"] = trend_data["breakdown_by_region"][0]["keyword"]

   # Related topics
   rt_data = flatten_topic_data(trend_data["related_topics"])
   rt_df = pd.DataFrame(rt_data)

   # Related queries
   rq_df = pd.DataFrame(trend_data["related_queries"][0]["items"])
   rq_df["keyword"] = trend_data["related_queries"][0]["keyword"]

   keyword = trend_data["interest_over_time"][0]["keyword"]
   keyword_path = os.path.join(CSV_FILE_DIR, keyword)
   try:
       os.makedirs(keyword_path, exist_ok=True)
   except OSError as e:
       print("Caught exception while creating directories")
       raise e

   print("Dumping to csv..")
   iot_df.to_csv(f"{keyword_path}/interest_over_time.csv", index=False)
   bbr_df.to_csv(f"{keyword_path}/breakdown_by_region.csv", index=False)
   rt_df.to_csv(f"{keyword_path}/related_topics.csv", index=False)
   rq_df.to_csv(f"{keyword_path}/related_queries.csv", index=False)

   result_set = {}
   result_set["iot"] = iot_df
   result_set["bbr"] = bbr_df
   result_set["rt"] = rt_df
   result_set["rq"] = rq_df

   return result_set


def create_comparison(trend_dataframes: dict) -> None:
    comparison = trend_dataframes[0]
    i = 1

    for df in trend_dataframes[1:]:
        comparison["iot"] = pd.merge(comparison["iot"], df["iot"], on="time", suffixes=("", f"_{i}"))
        comparison["bbr"] = pd.merge(comparison["bbr"], df["bbr"], on="geo_code", suffixes=("", f"_{i}"))

        if not df["rt"].empty and "title" in df["rt"].columns:
            comparison["rt"] = pd.merge(comparison["rt"], df["rt"], on="title", how="inner", suffixes=("", f"_{i}"))
        
        if not df["rq"].empty and "query" in df["rq"].columns:
            comparison["rq"] = pd.merge(comparison["rq"], df["rq"], on="query", how="inner", suffixes=("", f"_{i}"))

        i = i + 1

    comparison["iot"].to_csv("comparison_interest_over_time.csv", index=False)
    comparison["bbr"].to_csv("comparison_breakdown_by_region.csv", index=False)
    comparison["rt"].to_csv("comparison_related_topics.csv", index=False)
    comparison["rq"].to_csv("comparison_related_queries.csv", index=False)

