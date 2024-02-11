from Order import Order

class OrderBook:
    def __init__(self):
        self.head_bid = None
        self.head_offer = None

    def get_node(self, data):
        return Order(data)

    def insert(self, data):
        new_order = self.get_node(data)
        if data.get("side") == "BUY":
           self.insert_bid(new_order) 
        else:
            self.insert_offer(new_order)
        
    def insert_bid(self, order):
        if self.head_bid is None:
            self.head_bid = order
            return
        
        # new order price is higher, insert at front of list 
        elif self.head_bid.get("price") < order.get("price"):
            order.next = self.head_bid
            order.next.prev = order 
            self.head_bid = order

        else:
            current = self.head_bid
            next = current.next 
            while (next is not None) and (next.get("price") > order.get("price")):
                current = current.next

            order.next = current.next

            if current.next is not None:
                order.next.prev = order

            current.next = order
            order.prev = current

    def insert_offer(self, order):
        if self.head_offer is None:
            self.head_offer = order
            return
        
        # new order price is lower
        elif self.head_offer.get("price") > order.get("price"):
            order.next = self.head_offer
            order.next.prev = order 
            self.head_offer = order

        else:
            current = self.head_offer
            next = current.next 
            while (next is not None) and (next.get("price") < order.get("price")):
                current = current.next

            order.next = current.next

            if current.next is not None:
                order.next.prev = order

            current.next = order
            order.prev = current

    def print_book(self):
        self.print_side("BUY")
        print("\n\n")
        self.print_side("SELL")

    def print_side(self, side):
        if side == "BUY":
            node = self.head_bid
        else:
            node = self.head_offer
        while node:
            print(str(node.data), end = " ")
            node = node.next

if __name__ == "__main__":
    order = {"qty": 1, "price": 1.00, "side": "BUY"}
    order2 = {"qty": 1, "price": 0.95, "side": "BUY"}
    order3 = {"qty": 1, "price": 0.90, "side": "SELL"}
    order4 = {"qty": 1, "price": 0.92, "side": "SELL"}
    book = OrderBook()
    book.insert(order)
    book.insert(order2)
    book.insert(order3)
    book.insert(order4)
    book.print_book()

    # TODO - match the order if the spread is crossed
    # Add orders based on time
    