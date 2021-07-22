import stripe
from functools import wraps

stripe.api_key = os.getenv("STRIPE_KEY")


def stripe_handler(stripe_fn):
    @wraps(stripe_fn)
    def wrapper(*args, **kwargs):
        try:
            # Use Stripe's library to make requests...
            x = stripe_fn(*args, **kwargs)
            return x
            pass
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught

            print('Status is: %s' % e.http_status)
            print('Code is: %s' % e.code)
            # param is '' in this case
            print('Param is: %s' % e.param)
            print('Message is: %s' % e.user_message)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return e
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            return e.user_message
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return e
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return e
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return e
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            return e

    return wrapper


class StripePayments:
    def __init__(self, amount=None, currency=None, source=None, description=None, transact_id=None, refund=None):
        self.amount = amount
        self.currency = currency
        self.source = source
        self.description = description
        self.transact_id = transact_id
        self.refund = refund

    @stripe_handler
    def create_change(self):
        stripe_object = stripe.Charge.create(
          amount=self.amount,
          currency=self.currency,
          source=self.source,
          description=self.description,
        )
        return stripe_object

    @stripe_handler
    def capture_charge(self):
        stripe_object = stripe.Charge.capture(
              self.transact_id,
            )
        return stripe_object

    @stripe_handler
    def intiate_refund(self):
        stripe_object = stripe.Refund.create(
            self.refund,
        )
        return stripe_object

    @stripe_handler
    def get_all_charges(self):
        res = []
        retrive_users = True
        while retrive_users:
            retrive_users = stripe.Charge.list(limit=100)
            if retrive_users:
                res.extend(retrive_users)
            else:
                break
        return res
