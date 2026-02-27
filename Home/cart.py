from decimal import Decimal

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def clear(self):
        if 'session_key' in self.session:
            del self.session['session_key']
            self.session.modified = True

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price), 'qty': int(quantity)}
        else:
            self.cart[product_id]['qty'] += int(quantity)
        self.save()

    def update(self, product_id, action):
        p_id = str(product_id)
        if p_id in self.cart:
            if action == "plus":
                self.cart[p_id]['qty'] += 1
            elif action == "minus":
                self.cart[p_id]['qty'] -= 1
                if self.cart[p_id]['qty'] < 1: self.cart[p_id]['qty'] = 1
        self.save()

    def delete(self, product_id):
        p_id = str(product_id)
        if p_id in self.cart:
            del self.cart[p_id]
        self.save()

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def save(self):
        self.session.modified = True