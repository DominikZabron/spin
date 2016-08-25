# Simple spin game

This is simple casino game with free bonuses.

## Usage

### Install requirements

You need to have PostgreSQL database server installed and running

    pip install -r requirements.txt

### Run server

    cd spin
    export FLASK_APP=__init__.py
    flask run

### Tests

To run tests:

    nosetests --with-coverage --cover-package=spin

