from sanic import Blueprint
from sanic.app import Sanic

from services.constants import SERVICE

from resources.payment_view import PaymentCreditChargeView, PaymentChargeUtilView, PaymentRefundView, PaymentChargeView


def load_api(app: Sanic):
    api_prefix = "{service_name}/v1".format(service_name=SERVICE)

    api_v1 = Blueprint("v1", url_prefix=api_prefix)

    api_v1.add_route(PaymentCreditChargeView.as_view(), "/create_charge", strict_slashes=False)

    api_v1.add_route(PaymentChargeUtilView.as_view(), "/capture_charge/<id>", strict_slashes=False)

    api_v1.add_route(PaymentRefundView.as_view(), "/create_refund/<id>", strict_slashes=False)

    api_v1.add_route(PaymentChargeView.as_view(), "/get_charges", strict_slashes=False)

    app.blueprint(api_v1)