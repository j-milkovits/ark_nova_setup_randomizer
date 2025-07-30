# Ark Nova - Setup Randomizer
> simple application to make the setup of physical Ark Nova easier

## Features
- Randomize Map Assignment
- Supports Alternative Maps
- Supports Map Pack 1 & 2
- Randomize Starting Player
- Options to only use certain parts of the randomizer
- Randomize Bonus Tiles
- Randomize Base Conservation Project Cards
- Supports Marine World
- Dockerized Application for easy deployment

## Usage
### Demo
You can find a deployed application to use as much as you want at [Link]().

### Local
```bash
# setup your local environment e.g. using uv or poetry
uv sync

# enter local environment and start using make
source .venv/bin/activate
make run_locally
```

### Docker
```bash
# build using make
make build_docker

# start using make
make run_docker

# or use
make build_and_run_docker
```

## Contributing
```bash
# make sure to install the development dependencies

# make sure to setup the pre-commit hooks
pre-commit install
```
