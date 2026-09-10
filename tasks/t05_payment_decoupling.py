# Task 5: Decoupled Payment Gateway Adapter
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount_cents: int, currency: str, token: str) -> dict:
        pass

class MockStripeAdapter(PaymentGateway):
    def charge(self, amount_cents: int, currency: str, token: str) -> dict:
        if not token.startswith("tok_"):
            raise ValueError("Invalid Stripe token")
        return {"status": "succeeded", "charge_id": f"ch_{token[-6:]}", "amount": amount_cents}

class CheckoutService:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def process_order(self, amount_cents: int, token: str):
        return self.gateway.charge(amount_cents, "USD", token)
