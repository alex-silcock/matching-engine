from Order import Order

class OrderBook:
    def __init__(self):
        self.head_bid = None
        self.head_offer = None

    def create_order(self, data):
        return Order(data)

    def get_fair_price(self):
        return round((self.get_best_bid() + self.get_best_offer()) / 2, 5)

    def get_best_bid(self):
        return self.head_bid.get("price") if self.head_bid else -1

    def get_best_offer(self):
        return self.head_offer.get("price") if self.head_offer else -1

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
            if (self.get_best_offer() != -1) and new_order_price >= self.best_offer:
                self.handle_spread_cross("SELL", new_order)
                return
            self.insert_bid(new_order) 
        else:
            if (self.get_best_bid() != -1) and new_order_price <= self.best_bid:
                self.handle_spread_cross("BUY", new_order)
                return
            self.insert_offer(new_order)
    
    def handle_spread_cross(self, side, order):
        orders_traded = []
        qty_left_to_trade = order.get("qty")
        if side == "BUY":
            current = self.head_bid
            while qty_left_to_trade:
                current_trade_qty = current.get("qty")
                current_trade_id = current.get("trade_id")
                current_trade_side = current.get("side")
                if qty_left_to_trade >= current_trade_qty:
                    orders_traded.append(current_trade_id)
                    self.cancel_order(current_trade_id, current_trade_side)
                    qty_left_to_trade -= current_trade_qty
                    order.set("qty", qty_left_to_trade)
                    current = current.next
                    self.add(order)

                # cur trade has more qty than what's left to be traded 5 < 10
                else:
                    orders_traded.append(current_trade_id)
                    diff = min(qty_left_to_trade, current_trade_qty) * -1
                    self.update_quantity(current, diff=diff)
                    qty_left_to_trade = 0


        elif side == "SELL":
            return            
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
        if self.head_bid is None:
            self.head_bid = order
            self.best_bid = bid_price
        
        # new order price is higher, insert at front of list 
        elif bid_price > self.head_bid.get("price"):
            order.next = self.head_bid
            order.next.previous = order
            self.head_bid = order
            self.best_bid = bid_price

        else:
            current = self.head_bid
            next = current.next 
            while (next is not None) and (next.get("price") > bid_price):
                current = current.next

            order.next = current.next

            if current.next is not None:
                order.next.previous = order

            current.next = order
            order.previous = current

    def insert_offer(self, order):
        offer_price = order.get("price")
        if self.head_offer is None:
            self.head_offer = order
            self.best_offer = offer_price
            return
        
        # new order price is lower
        elif order.get("price") < self.head_offer.get("price"):
            self.best_offer = offer_price 
            order.next = self.head_offer
            order.next.previous = order 
            self.head_offer = order

        else:
            current = self.head_offer
            next = current.next 
            while (next is not None) and (next.get("price") < offer_price):
                current = current.next

            order.next = current.next

            if current.next is not None:
                order.next.previous = order

            current.next = order
            order.previous = current


    def print_book(self):
        self.print_side("BUY")
        print("\n\n")
        self.print_side("SELL")
        print("\n\n")

    def print_side(self, side):
        if side == "BUY":
            node = self.head_bid
        else:
            node = self.head_offer
        while node:
            print(str(node.data), end = "\n")
            node = node.next

if __name__ == "__main__":
    orders = [
        {"qty": 1, "price": 0.80, "side": "BUY"},
        {"qty": 1, "price": 0.90, "side": "BUY"},
        {"qty": 1, "price": 1.90, "side": "BUY"},
        {"qty": 0.5, "price": 0.89, "side": "SELL"},
        # TODO - this below order doesnt work - there is 0.5 to buy at 
        # 1.9 and it wipes the bids at 1.9 AND 0.9
        {"qty": 1, "price": 1.20, "side": "SELL"}
    ]
    book = OrderBook()
    for order in orders:
        book.add(order)
    book.print_book()
    print("Best Bid: ", book.get_best_bid())
    print("Best Offer: ", book.get_best_offer())
    print("Fair Price: ", book.get_fair_price())

    # TODO - match the order if the spread is crossed
    # Add orders based on time
    