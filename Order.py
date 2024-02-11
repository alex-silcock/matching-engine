import uuid
from datetime import datetime


class Order:
    def __init__(self, data):
        self.data = data
        self.data['time'] = datetime.now()
        self.data['trade_id'] = uuid.uuid4()
        self.next = None
        self.previous = None


    def get(self, var):
        return self.data.get(var)


    def set(self, var, val):
        self.data[var] = val