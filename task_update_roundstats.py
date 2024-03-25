from datetime import timedelta
import json

from loguru import logger

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from request_mixin import make_cached_limiter_session
import requests_cache
import toml

from model import Round

API_URL = "https://api.paradisestation.org/stats"

@logger.catch
def main():
    config = toml.load(open('config.toml'))
    connection_string = config['database']['prod_connection_string']

    logger.add("task_update_roundstats_{time}.log", rotation="12:00", serialize=True)
    rq_session = make_cached_limiter_session()

    engine = create_engine(connection_string)
    session = Session(engine)
    logger.info("getting roundstats")
    rounds = rq_session.get(f"{API_URL}/roundlist?offset=38348", expire_after=timedelta(hours=1)).json()
    for round in rounds:
        round_id = round['round_id']
        r = session.get(Round, round_id)
        if not r:
            logger.info(f"getting stats round_id={round_id}")
            Round.download(round_id)

if __name__ == "__main__":
    main()