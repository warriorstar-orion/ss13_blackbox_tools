# ss13_blackbox_tools

This repo contains scripts and libraries for working with Parastats.

## Basic Setup

1. Create a local database with the same schema as Paradise itself (https://github.com/ParadiseSS13/Paradise/blob/master/SQL/paradise_schema.sql).
2. Copy `config.example.toml` over to `config.toml` and set the connection string appropriately.
3. Create the appropriate Python environment, installing dependencies from `requirements.txt`.
4. Set up a cronjob/Windows scheduled task to run `task_update_roundstats.py` once a day. Once a day is enough.
5. Check `nukie_round_items.ipynb` for an example on how to perform some stats crunching.