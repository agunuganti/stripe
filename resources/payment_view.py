from controller.stripe import StripePayments
from resources.base_view import BaseView


class PaymentCreditChargeView(BaseView):

    async def post(self, request):
        body = request.json
        payment_controller = StripePayments(amount=body["amount"], currency=body["currency"], source=body["source"],
                                            description=body["description"])
        data = payment_controller.create_change()
        return self.get_response(data)


class PaymentChargeUtilView(BaseView):

    async def post(self, request, id):
        body = request.json
        payment_controller = StripePayments(transact_id=id)
        data = payment_controller.capture_charge()
        return self.get_response(data)


class PaymentRefundView(BaseView):

    async def post(self, request, id):
        payment_controller = StripePayments(refund=id)
        data = payment_controller.intiate_refund()
        return self.get_response(data)


class PaymentChargeView(BaseView):

    async def get(self, request):
        payment_controller = StripePayments()
        data = payment_controller.get_all_charges()
        return self.get_response(data)