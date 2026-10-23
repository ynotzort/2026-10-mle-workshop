# 2026-10-mle-workshop

# day 1

this project is based on https://github.com/ynotzort/ml-engineering-contsructor-workshop

## how to install uv

just run `curl -LsSf https://astral.sh/uv/install.sh | sh`

## day 1 steps

### get the notebook
- create a new folder `day_1` (`mkdir day_1`)
- change directory into `day_1` (`cd day_1`)
- get the original notebook:
```bash
mkdir notebooks
cd notebooks
wget "https://github.com/ynotzort/ml-engineering-contsructor-workshop/raw/main/01-train/duration-prediction-starter.ipynb"
cd ..
```

### create a uv project
- initialize a uv project with `uv init --python 3.10`
- run `uv sync`

### install dependencies
- `uv add scikit-learn==1.2.2 pandas pyarrow`
- `uv add --dev jupyter seaborn`
- now lets fix the error with numpy: `uv add numpy==1.26.4`

### launch jupyter notebook
- `uv run jupyter notebook`

### make vscode recognize the python env correctly and use jupyter from within vscode
- open .py file (`day_1/src/day_1/__init__.py`)
- on the bottom right click on the python version -> browse -> find the path to python (here it was `/workspaces/2026-10-mle-workshop/day_1/.venv/bin/python`)
- go to jupyter notebook file and click select kernel -> python environments -> day 1

### convert the notebook into a python script
- `uv run jupyter nbconvert --to=script notebooks/duration-prediction-starter.ipynb`
- move the freshly created file into the src/day_1 folder: `mv notebooks/duration-prediction-starter.py src/day_1/`
- lets rename it to train.py: `mv src/day_1/duration-prediction-starter.py src/day_1/train.py`

### lets make the train.py script nice
- remove all the # In[] lines from the script
- move all the imports to top and clean up in general
- get rid of matplotlib and seaborn
- try to run the script: `uv run python src/day_1/train.py`
- create a train function and entrypoint `if __name__=="__main__":`
- introduce pipeline code
- parametrize the train function
- use argparse for parsing, and call via `uv run python src/day_1/train.py --train-date=2022-01 --val-date=2022-02 --model-save-path=model.pkl`
    - alternatives are https://github.com/fastapi/typer and fire.
- create a model folder: `mkdir models` and use `uv run python src/day_1/train.py --train-date=2022-01 --val-date=2022-02 --model-save-path=models/2022-01.pkl`
- add typing and docstrings
- add simple error handling
- add logging: `uv add loguru`
- split out the argparse into main.py. now we can run it via `uv run python src/day_1/main.py --train-date=2022-01 --val-date=2022-02 --model-save-path=models/2022-01.pkl` or alternativel using the module mode: `uv run python -m src.day_1.main --train-date=2022-01 --val-date=2022-02 --model-save-path=models/2022-01.pkl`

### create a Makefile
- `touch Makefile`
- now we can train via just `make train`

### tests
- `uv add pytest`
- `mkdir tests`
- create a `__init__.py` inside of tests/ folder (`touch tests/__init__.py`)
- create a `test_train.py` file inside of the tests folder (has to start with `test_`) (`touch tests/test_train.py`)
- run tests with `uv run pytest` or `make test`


# day 2

## create the project and add the dependencies
- create a new top level folder `day_2` just below `day_1` and cd into it: `mkdir day_2 && cd day_2`
- create a new uv project: `uv init --lib --python 3.10 duration_pred_serve`
- change into this newly created folder: `cd duration_pred_serve`
- add dependencies from day_1: `uv add scikit-learn==1.2.2 numpy==1.26.4`
- lets add the testing and logging dependcies: `uv add loguru pytest`
- add webserver dendency: `uv add "fastapi[standard]"`
- for debugging lets add requests dependency: `uv add --dev requests`
- copy over the model from day_1 here: `mkdir models && cp ../../day_1/models/2022-01.pkl models/`

## ping example for fastAPI
- create a `ping.py` file insider of `src/duration_pred_serve/` and open it
- change the python virtual environment to use the correct day 2 environment. click on the bottom right where it says day_1 and then click browse and select `/workspaces/2026-10-mle-workshop/day_2/duration_pred_serve/.venv/bin/python`
- run it via `uv run fastapi dev src/duration_pred_serve/ping.py`

## implement serve
- implementing simple loading of the model file and run it via `uv run python src/duration_pred_serve/serve.py`
- make it a webserver and run it `uv run fastapi dev src/duration_pred_serve/serve.py` or `make serve`

## environment variables
- you can create environment variables via the export command: `export HELLO=world`, this creates a variable named `HELLO` wiith the value of "world"
- print out the value of the variable with `echo $WORLD` (note the dollar sign)
- remove the variable via `unset HELLO`
- in python you can access the environment variables via `os.getenv()`
- alternatively we can use `BaseSettings` from the package `pydantic_settings`
- now we can define the model path via `export MODEL_PATH=models/2022-01.pkl`
- lets add it to the Makefile
- add the MODEL_VERSION also

## implement a predict test with requests
- lets make a folder scripts `mkdir scripts`
- inside of it lets create a `predict-test.py` file (`touch scripts/predict-test.py`)
- we can run it via `uv run python scripts/predict-test.py`

## use Docker
- create a Dockerfile
- build the image via `docker build -t duration-prediction:latest .`
- run it via `docker run -it duration-prediction:latest`
- or just use `make docker-run` which will first build the image and then run it
- modeify the dockerfile to use uv and our own project

## lets deploy it to the world via fly.io
- install it via `curl -L https://fly.io/install.sh | sh` and then run as suggested `source ~/.bashrc`
- login via `fly auth login`
- deploy the app via `fly launch`
