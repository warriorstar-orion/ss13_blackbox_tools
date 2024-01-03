from datetime import timedelta
import json

from loguru import logger

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import requests_cache

from model import *

API_URL = "https://api.paradisestation.org/stats"

@logger.catch
def main():
    logger.add("task_update_roundstats_{time}.log", rotation="12:00", serialize=True)
    rq_session = requests_cache.CachedSession('api_paradisestation_org_roundstat_')
    engine = create_engine("mysql+mysqldb://root@localhost/parastats_prod")
    session = Session(engine)
    logger.info("getting roundstats")
    rounds = rq_session.get(f"{API_URL}/roundlist", expire_after=timedelta(hours=1)).json()
    for round in rounds:
        round_id = round['round_id']
        r = session.get(Round, round_id)
        if not r:
            logger.info(f"getting stats round_id={round_id}")
            Round.download(round_id)

if __name__ == "__main__":
    main()