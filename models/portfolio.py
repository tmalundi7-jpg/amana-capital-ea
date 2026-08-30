from datetime import datetime

class Portfolio:
    def __init__(self, client_id):
        self.client_id = client_id
        self.total_value = 0.0
        self.assets = []
        self.last_updated = datetime.utcnow()

    def add_asset(self, symbol, quantity, current_price):
        self.assets.append({'symbol': symbol, 'quantity': quantity, 'price': current_price})
        self.recalculate()

    def recalculate(self):
        self.total_value = sum(asset['quantity'] * asset['price'] for asset in self.assets)
        self.last_updated = datetime.utcnow()
