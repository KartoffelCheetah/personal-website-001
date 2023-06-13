# personal-website-001

## Setup

```bash
git submodule init
git submodule update
cp .env.dist .env
# edit the .env file
mkdir .venv database/storage
./container_setup.sh
```

## Cli Tasks

```bash
# podman container exec pw001_python pipenv run flask image --help
podman container exec pw001_python pipenv run flask image status
podman container exec pw001_python pipenv run flask image fs2db
```
