from datetime import timedelta, datetime

import click
import typed_settings as ts
from loguru import logger
from sqlalchemy import create_engine

from ss13tools.request_mixin import make_cached_limiter_session
from ss13tools.model import ProfilerSample, Round
from ss13tools.settings import SS13ToolsSettings, make_engine

from sqlalchemy import create_engine
from sqlalchemy import desc, asc
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session, lazyload, joinedload

# settings = ts.load(SS13ToolsSettings, appname="ss13tools", config_files=["settings.toml"])
# engine = make_engine("settings.toml")
# session = Session(engine)
# session.scalars(select(Round).order_by(~Round.id).limit(100))
# latest_round_ids = session.scalars(select(Round).order_by(~Round.id).limit(100))
# [x.id for x in latest_round_ids]
# [x.id for x in latest_round_ids.unique()]
# latest_round_ids = session.scalars(select(Round).order_by(~Round.id).limit(100).unique())
# latest_round_ids = session.scalars(select(Round).order_by(~Round.id).limit(100)).unique()
# [x.id for x in latest_round_ids.unique()]
# [x.id for x in latest_round_ids]
# [x.id for x in latest_round_ids.unique()]
# latest_round_ids = list(session.scalars(select(Round).order_by(~Round.id).limit(100)).unique())
# latest_round_ids
# latest_round_ids = session.scalars(select(Round).order_by(~Round.id).limit(100)).unique()
# [x.id for x in latest_round_ids]
# [x.id for x in latest_round_ids]
# latest_round_ids = session.scalars(select(Round).order_by(~Round.id).limit(100)).unique()
# round_ids = [x.id for x in latest_round_ids]
# sorted(round_ids)
# latest_round_ids = session.scalars(select(Round).order_by(~Round.id).limit(100))
# round_ids = [x.id for x in latest_round_ids]
# print(select(Round).order_by(~Round.id).limit(100))
# print(select(Round).order_by(Round.id.asc).limit(100))
# print(select(Round).order_by(Round.id.asc()).limit(100))
# print(select(Round).order_by(Round.id.desc()).limit(100))
# latest_round_ids = session.scalars(select(Round).order_by(Round.id.desc()).limit(100))
# round_ids = [x.id for x in latest_round_ids]
# latest_round_ids = session.scalars(select(Round).order_by(Round.id.desc()).limit(100)).unique()
# round_ids = [x.id for x in latest_round_ids]
# sorted(round_ids)
# from ss13tools.request_mixin import make_cached_limiter_session
# rq_session = make_cached_limiter_session()
# min(round_ids)
# api_url = settings.api_url
# rq_session.get(f"{api_url}/profiler/getproc", expire_after=timedelta(hours=1)).json()
# from datetime import date, datetime, timedelta
# rq_session.get(f"{api_url}/profiler/getproc", expire_after=timedelta(hours=1)).json()
# rq_session.get(f"{api_url}/profiler/getproc", expire_after=timedelta(hours=1))
# api_url
# api_url = 'https://api.paradisestation.org'
# rq_session.get(f"{api_url}/profiler/getproc", expire_after=timedelta(hours=1))
# response = rq_session.get(f"{api_url}/profiler/getproc", expire_after=timedelta(hours=1))
# response.json()
# response.text
# response = rq_session.get(f"{api_url}/profiler/getproc", params={'procname': "/datum/controller/subsystem/mapping/proc/loadStation"}, expire_after=timedelta(hours=1))
# response.text
# response = rq_session.get(f"{api_url}/profiler/getproc", params={'procname': "/datum/controller/subsystem/mapping/proc/loadStation", 'roundid': "42260"}, expire_after=timedelta(hours=1))
# response
# response.json()
# min(round_ids)
# earliest_round = min(round_ids)
# select(ProfilerSample).filter
# select(ProfilerSample).filter(round_id=earliest_round)
# select(ProfilerSample).filter(round_id==earliest_round)
# select(ProfilerSample).filter(ProfileSampler.round_id==earliest_round)
# select(ProfilerSample).filter(ProfileSample.round_id==earliest_round)
# select(ProfilerSample).filter(ProfilerSample.round_id==earliest_round)
# print(select(ProfilerSample).filter(ProfilerSample.round_id==earliest_round))
# session.scalar(select(ProfilerSample).filter(ProfilerSample.round_id==earliest_round)).count())
# session.scalar(select(ProfilerSample).filter(ProfilerSample.round_id==earliest_round)).count()
# session.scalar(select(ProfilerSample).filter(ProfilerSample.round_id==earliest_round).count())
# session.scalar(select(ProfilerSample).filter(ProfilerSample.round_id==earliest_round))
# session.scalar(select(ProfilerSample).filter(ProfilerSample.round_id==earliest_round)).count
# result = session.scalar(select(ProfilerSample).filter(ProfilerSample.round_id==earliest_round))
# result
# response
# response.json()
# with Session(engine, expire_on_commit=False) as session:
#     for data in response.json():
#         sample = ProfilerSample(round_id=data['roundId'],
#             sample_time=data['sampleTime'],
#             proc_path=data['procpath'],
#             self_cpu=data['self'],
#             total_cpu=data['total'],
#             real_time=data['real'],
#             overtime=data['over'],
#             proc_calls=data['calls'])
#         session.add(sample)
#         session.commit()


@click.command()
@click.option(
    "--settings_file", required=True, help="Location of your settings.toml file."
)
@logger.catch
def main(settings_file):
    settings: SS13ToolsSettings = ts.load(
        SS13ToolsSettings, appname="ss13tools", config_files=[settings_file]
    )

    logger.add(
        "task_update_profilesamples.log",
        rotation="weekly",
        retention="10 days",
        serialize=True,
    )

    engine = create_engine(settings.connection_string)

    logger.info("getting profile data...")

    with Session(engine, expire_on_commit=False) as session:
        get_profile_data(session, settings)


def get_profile_data(session: Session, settings: SS13ToolsSettings):
    rq_session = make_cached_limiter_session()
    api_url = settings.api_url
    latest_rounds = session.scalars(
        select(Round).order_by(Round.id.desc()).limit(100)
    ).unique()
    latest_round_ids = [x.id for x in latest_rounds]

    for round_id in latest_round_ids:
        profiler_samples = session.scalar(
            select(ProfilerSample).filter(ProfilerSample.round_id == round_id)
        )
        if profiler_samples:
            return

        for proc_name in settings.profile_proc_paths:
            response = rq_session.get(
                f"{api_url}/profiler/getproc",
                params={"procname": proc_name, "roundid": str(round_id)},
                expire_after=timedelta(hours=1),
            )

            if response.status_code == 200:
                for data in response.json():
                    sample = ProfilerSample(
                        round_id=data["roundId"],
                        sample_time=data["sampleTime"],
                        proc_path=data["procpath"],
                        self_cpu=data["self"],
                        total_cpu=data["total"],
                        real_time=data["real"],
                        overtime=data["over"],
                        proc_calls=data["calls"],
                    )
                    session.add(sample)
                    session.commit()

                logger.info(f"downloaded round_id={round_id} proc_name={proc_name}")
            elif response.status_code == 404:
                logger.info(f"stopping at missing round_id={round_id}")
                return


if __name__ == "__main__":
    main()
