from datetime import timedelta

from loguru import logger

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from request_mixin import make_cached_limiter_session
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
    logger.info("getting roundstats")
    rounds = rq_session.get(f"{API_URL}/roundlist", expire_after=timedelta(hours=1)).json()
    for round in rounds:
        round_id = round['round_id']
        downloaded = Round.download(engine, round_id, rq_session)
        if downloaded:
            logger.info(f"downloaded round_id={round_id}")

if __name__ == "__main__":
    main()