from datetime import timedelta, datetime

import click
import typed_settings as ts
from loguru import logger
from sqlalchemy import create_engine

from ss13tools.request_mixin import make_cached_limiter_session
from ss13tools.model import Round
from ss13tools.settings import SS13ToolsSettings, make_engine

from sqlalchemy import create_engine
from sqlalchemy import desc, asc
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session, lazyload, joinedload

STOP_DATE = datetime(2018, 3, 23)

@click.command()
@click.option('--settings_file', required=True, help='Location of your settings.toml file.')
@logger.catch
def main(settings_file):
    settings: SS13ToolsSettings = ts.load(SS13ToolsSettings, appname="ss13tools", config_files=[settings_file])

    logger.add("task_update_roundstats.log", rotation="weekly", retention="10 days", serialize=True)
    rq_session = make_cached_limiter_session()

    # engine = make_engine(settings_file)

    # session = Session(engine)
    # first_round = session.query(Round).order_by(asc(Round.initialize_datetime)).first()

    # earliest_download = first_round.initialize_datetime
    # earliest_round = first_round.id

    engine = create_engine(settings.connection_string)
    api_url = settings.api_url
    logger.info("getting roundstats...")
    # while earliest_download > STOP_DATE:
    rounds = rq_session.get(f"{api_url}/stats/roundlist", expire_after=timedelta(hours=1)).json()
    for round in rounds:
        round_id = round['round_id']
        logger.info(f"round_id={round_id}")
        downloaded = Round.download(engine, round_id, rq_session, api_url)
        if downloaded:
            logger.info(f"downloaded round_id={round_id}")
            # earliest_round = downloaded.id
            # earliest_download = datetime.strptime(downloaded.initialize_datetime, '%Y-%m-%dT%H:%M:%S')

if __name__ == "__main__":
    main()
