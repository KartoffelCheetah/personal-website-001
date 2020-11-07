"""ENV loading"""
from typing import Final
from dotenv import load_dotenv, dotenv_values
from app.definitions import PROJECT_PATH

def load_env():
    """Reads the configuration
    and overrides ENVIRONMENT variables with dotenv.load_dotenv.
    """
    ENV: Final[str] = '.env'
    DIST: Final[str] = '.env.dist'
    env: Final[dict] = dotenv_values(PROJECT_PATH/ENV)
    dist: Final[dict] = dotenv_values(PROJECT_PATH/DIST)

    if env.keys() == dist.keys():
        load_dotenv(dotenv_path=PROJECT_PATH/ENV, override=True)
    else:
        raise KeyError(f'{ENV} and {DIST} schema does not match')
