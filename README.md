# Auth Service

## Creation of virtual environments

`uv venv`

## Install

`uv sync`

## Configure env

Example: [env](env.example)

## Apply migrations

`alembic upgrade head`

## Run

`uvicorn --factory app.main:get_app --reload`
