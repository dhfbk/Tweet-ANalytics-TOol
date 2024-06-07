import os
import json
import logging

from fastapi import FastAPI, HTTPException, Header, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

import log_conf
import utils

logging.config.dictConfig(log_conf.log_config)

logger = logging.getLogger('sbm2-logger')

load_dotenv()

data_path = os.environ.get("DATA_PATH", "./data")

main_data = {}
listFile = os.path.join(data_path, "datasets.json")
with open(listFile) as f:
    main_data = json.load(f)

lang_data = {}
listFile = os.path.join(data_path, "languages.json")
with open(listFile) as f:
    lang_data = json.load(f)


logger.info("Loading data...")
datasets = {}
for k in main_data:
    logger.info(f"Loading dataset {k}")
    datasets[k] = utils.load_data(os.path.join(data_path, k))

logger.info("Starting API...")

# Allow CORS for all origins
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins = ['*'],
        allow_methods = ['*'],
        allow_headers = ['*'],
        expose_headers = ['access-control-allow-origin'],
    )
]

app = FastAPI(middleware=middleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/datasets")
async def get_data():
    return main_data

@app.get("/api/languages")
async def get_data():
    return lang_data

@app.get("/api/dataset/{dataset_id}")
async def get_data(dataset_id: str, d0: str = None, d1: str = None, words: str = None):
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
    myReturn = utils.plot_dataset(datasets[dataset_id], main_data[dataset_id], d0, d1, words)
    if not myReturn:
        raise HTTPException(status_code=422, detail=f"No information for the selected filters.")
    return myReturn
    # try:
    #     return utils.plot_dataset(datasets[dataset_id], main_data[dataset_id], d0, d1, words)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=repr(e))


from fastapi.responses import HTMLResponse

@app.get("/api/hashtag/{dataset_id}", response_class=HTMLResponse)
async def get_data(dataset_id: str, d0: str = None, d1: str = None, words: str = None):
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
    myReturn = utils.get_htnet(datasets[dataset_id], main_data[dataset_id], d0, d1, words)
    if not myReturn:
        raise HTTPException(status_code=422, detail=f"No information for the selected filters.")
    return myReturn

@app.get("/api/retweet/{dataset_id}", response_class=HTMLResponse)
async def get_data(dataset_id: str, d0: str = None, d1: str = None, words: str = None):
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
    return utils.get_rtnet(datasets[dataset_id], main_data[dataset_id], d0, d1, words)

@app.get("/api/wordcloud/{dataset_id}",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    }, response_class=Response)
async def get_data(dataset_id: str, d0: str = None, d1: str = None, words: str = None):
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
    image_bytes: bytes = utils.get_wc(datasets[dataset_id], main_data[dataset_id], d0, d1, words)
    return Response(content=image_bytes, media_type="image/png")
