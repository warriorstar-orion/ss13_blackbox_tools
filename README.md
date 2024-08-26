# ss13_blackbox_tools

This repo contains scripts and libraries for working with Parastats.

## Configuration Settings

`ss13_blackbox_tools` requires some information about your environment in order
to work properly:

- `api_url` is the URL of the Parastats API. This will probably never change
  from its default.
- `working_directory` is where various library output is placed, such as the
  location of the API cache and task logs.
- `log_tasks` specifies whether you want tasks to output logs to the working
  directory.
- `connection_string` is the connection string to your Postgres database where
  you are storing round data.
- `paradise_root` is the path of your local Paradise codebase.

## API Cache

`ss13_blackbox_tools` uses an SQLite database to cache requests from the
Parastats API, and rate-limit the library so as to not flood the Parastats
server with requests.

## Basic Setup

To keep things simple, `ss13_blackbox_tools` uses the exact same schema as
Paradise itself. Round, feedback, and population data is returned from the API
in almost exactly the same format as what is stored by the game itself.

The database used is expected to be PostgreSQL. I have not tested with other
databases.

1. Create a local database with the same schema as Paradise itself
   (https://github.com/ParadiseSS13/Paradise/blob/master/SQL/paradise_schema.sql).
2. Copy `config.example.toml` over to `config.toml` and set the above
   configuration settings appropriately.
3. Set up a cronjob/Windows scheduled task to run `task_update_roundstats.py`
   once a day. Once a day is enough.
5. Check `nukie_round_items.ipynb` for an example on how to perform some stats
   crunching.
