import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
from utils.Order import Order

class OrderBook:
    def __init__(self):
        self.head_bid = None
        self.head_offer = None

    def create_order(self, data):
        return Order(data)

    def get_fair_price(self):
        best_bid, best_offer = self.get_best_bid(), self.get_best_offer()
        if best_bid and best_offer:
            return round((best_bid + best_offer) / 2, 5)
        return None

    def get_best_bid(self):
        return self.head_bid.get("price") if self.head_bid else None

    def get_best_offer(self):
        return self.head_offer.get("price") if self.head_offer else None

    def update_quantity(self, order, diff=None, new_qty=None):
        if diff:
            order.set("qty", order.get("qty") + diff)
            return
        elif new_qty:
            order.set("qty", new_qty)
            return

    def add(self, data):
        if not data.get("qty"):
            return
        
        if not isinstance(data, Order):
            new_order = self.create_order(data)
        else:
            new_order = data
        new_order_price = data.get("price")

        if data.get("side") == "BUY":
            best_offer = self.get_best_offer()
            if best_offer and new_order_price >= best_offer:
                self.handle_spread_cross("SELL", new_order)
                return
            self.insert_bid(new_order) 
        else:
            best_bid = self.get_best_bid()
            if best_bid and new_order_price <= best_bid:
                self.handle_spread_cross("BUY", new_order)
                return
            self.insert_offer(new_order)
    
    def handle_spread_cross(self, side_crossed, incoming_order):
        orders_traded = []
        qty_left_to_trade = incoming_order.get("qty")

        if side_crossed == "BUY":
            current = self.head_bid
        elif side_crossed == "SELL":
            current = self.head_offer

        while qty_left_to_trade:
            current_trade_qty = current.get("qty")
            current_trade_id = current.get("trade_id")
            current_trade_side = current.get("side")

            if qty_left_to_trade >= current_trade_qty:
                orders_traded.append(current_trade_id)
                self.cancel_order(current_trade_id, current_trade_side)
                qty_left_to_trade -= current_trade_qty
                self.update_quantity(incoming_order, new_qty=qty_left_to_trade)
                current = current.next

            # cur trade has more qty than what's left to be traded 5 < 10
            else:
                orders_traded.append(current_trade_id)
                diff = min(qty_left_to_trade, current_trade_qty) * -1
                self.update_quantity(current, diff=diff)
                qty_left_to_trade = 0
                    
        return orders_traded
        
    def cancel_order(self, trade_id, side):
        if side == "BUY":
            current = previous = self.head_bid
        else:
            current = previous = self.head_offer

        next = current.next
        if current and current.get("trade_id") == trade_id:
            if side == "BUY":
                self.head_bid = next
            else:
                self.head_offer = next
            current = None
            return
            
        while current:
            if current.get("trade_id") == trade_id:
                break
            previous = current
            current = current.next
        
        if not current:
            return
    
        previous.next = current.next
        current = None


    def insert_bid(self, order):
        bid_price = order.get("price")
        if not self.head_bid:
            self.head_bid = order
            self.head_bid.next = None
        
        # new order price is higher, insert at front of list 
        elif bid_price > self.head_bid.get("price"):
            order.next = self.head_bid
            order.next.previous = order
            self.head_bid = order

        else:
            current = self.head_bid
            next = current.next 
            while (next is not None) and (next.get("price") > bid_price):
                next = next.nexts
                current = current.next

            order.next = current.next
            current.next = order
            order.previous = current

    def insert_offer(self, order):
        offer_price = order.get("price")
        if not self.head_offer:
            self.head_offer = order
            self.head_offer.next = None
            return
        
        # new order price is lower
        elif order.get("price") < self.head_offer.get("price"):
            order.next = self.head_offer
            order.next.previous = order 
            self.head_offer = order

        else:
            current = self.head_offer
            next = current.next 
            while (next is not None) and (next.get("price") < offer_price):
                current = current.next
                next = next.next

            order.next = current.next
            current.next = order
            order.previous = current


    def print_book(self):
        print("BIDS:")
        self.print_side("BUY")
        print("\n")
        print("OFFERS:")
        print("\n")
        self.print_side("SELL")

    def print_side(self, side):
        if side == "BUY":
            node = self.head_bid
        elif side == "SELL":
            node = self.head_offer
        while node:
            print(str(node.data), end="\n")
            node = node.next


def main() -> None:
    orders = [
        {"qty": 1, "price": 0.80, "side": "SELL"},
        {"qty": 1, "price": 0.90, "side": "SELL"},
        {"qty": 1, "price": 1.00, "side": "SELL"},
        {"qty": 0.5, "price": 0.90, "side": "BUY"},
        {"qty": 1.5, "price": 1.20, "side": "BUY"}
    ]
    book = OrderBook()
    for order in orders:
        book.add(order)
    book.print_book()
    print("Best Bid: ", book.get_best_bid())
    print("Best Offer: ", book.get_best_offer())
    print("Fair Price: ", book.get_fair_price())

    # TODO - Add orders based on time
    
if __name__ == "__main__":
   main() 