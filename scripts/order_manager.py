from dataclasses import dataclass


@dataclass
class Order:
    side: str
    quantity: int
    price: float


class OrderManager:
    def __init__(self):
        self.orders = []

    def place_order(self, order: Order):
        self.orders.append(order)

    def cancel_all(self):
        self.orders.clear()
