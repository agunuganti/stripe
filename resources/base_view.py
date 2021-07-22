import datetime
from http import HTTPStatus

from sanic import response
from sanic.constants import HTTP_METHODS
from sanic.views import HTTPMethodView


class BaseView(HTTPMethodView):
    async def options(self, *args, **kwargs):
        headers = {"Access-Control-Allow-Methods": ", ".join(
            [method for method in HTTP_METHODS if hasattr(self, method.lower())]
        )}

        return response.text('', 200, headers=headers)

    def get_response(self, data, status=HTTPStatus.OK.value):
        return response.json(
            {
                'data': data,
                'response_datetime': datetime.datetime.utcnow().isoformat(),
                'status': 'success'
                if (status == HTTPStatus.OK.value or status == HTTPStatus.CREATED.value)
                else 'failed'
            },
            status=status
        )