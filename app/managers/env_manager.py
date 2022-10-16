"""ENV loading"""
from typing import Final
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
from app.definitions import PROJECT_PATH

def _load_env():
  """Reads the configuration
  and overrides ENVIRONMENT variables with dotenv.load_dotenv.
  This is a side-effect!
  """
  ENV: Final[str] = Path('/etc/')/Path(PROJECT_PATH).absolute().name/'.env'
  DIST: Final[str] = PROJECT_PATH/'.env.dist'
  env: Final[dict] = dotenv_values(ENV)
  dist: Final[dict] = dotenv_values(DIST)

  if env.keys() == dist.keys():
    load_dotenv(dotenv_path=ENV, override=True)
  else:
    raise KeyError(f'{ENV} and {DIST} schema does not match')

if __name__ != '__main__':
  _load_env()
else:
  raise ImportError('env_manager should be imported')
