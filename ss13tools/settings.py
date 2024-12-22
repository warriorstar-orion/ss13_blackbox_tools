from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import Engine
import typed_settings as ts

@ts.settings(frozen=True)
class SS13ToolsSettings:
    api_url: str
    working_directory: Path
    log_tasks: bool
    paradise_root: Path
    connection_string: str = ts.secret()
    profile_proc_paths: list[str]

    def api_cache(self):
        return self.working_directory / "api_paradisestation_org_roundstat.sqlite"


def make_engine(config_file: str | Path) -> Engine:
    settings = ts.load(SS13ToolsSettings, appname="ss13tools", config_files=[config_file])
    return create_engine(settings.connection_string)
