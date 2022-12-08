# search_app
Educational FastApi project with elasticsearch

# how to use: will be written soon...


## How to run locally
- put variables into .env (as well as elastic credentials)
- create virtual environment:
>... if using poetry
> - poety install
> - poetry shell

>... if using venv
> - python -m venv .venv
> - activate virtual environment
> - pip install -r requirenments.txt

- `make build`: builds docker containers, runs it and runs migrations

> first separated scripts: 
1. fill_db_from_csv.py
2. first_fill_index.py

(for the *task* it fills db with 
initial data of a given structure from csv doc, and then creates and fills index from initial db data)
if to run a FastApi app locally: - `make run` (but it can be ran in docker)


## Tools
- elasticsearch
- postgres
- alembic
- sqlalchemy
- asyncio
- docker-compose
- makefile
- poetry
- pytest

# The Task branch
- the app has two handlers: 
- for searching the match of a query with messages in elastic
- for deleting document from db and elastic by id

![Clipboard01](https://user-images.githubusercontent.com/8655093/202918040-709cc06c-d10f-427c-84d2-2d180ae005f8.jpg)

# The develop draft branch
- has a separated handlers for creating index in elastic, deleting it, showing all data (for debugging purposes)


![Clipboard02](https://user-images.githubusercontent.com/8655093/202918161-97245239-44cc-4976-ae86-a3c70c0bf7af.jpg)

