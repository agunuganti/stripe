import logging

from sanic.app import Sanic
from sanic_cors import CORS

from services import api
from services.constants import SERVICE




app = Sanic(SERVICE)
cors = CORS(
    app,
    resources = {r"*": {"origin": "*"}}
)

api.load_api(app)