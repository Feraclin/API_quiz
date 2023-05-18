import os
from pathlib import Path

from dotenv import load_dotenv

from api.app.schemas import ConfigEnv

env_name = ".env"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

dotenv_file = os.path.join(BASE_DIR, env_name)
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)
config_env = os.environ

config_api = ConfigEnv(
    db_host=config_env.get("POSTGRES_HOST"),
    db_port=int(config_env.get("POSTGRES_PORT")),
    db_user=config_env.get("POSTGRES_USER"),
    db_pass=config_env.get("POSTGRES_PASSWORD"),
    db=config_env.get("POSTGRES_DB"),
)
