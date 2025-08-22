from locust import HttpUser, task, between
import random
import string

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

class User(HttpUser):
    weight=9
    def on_start(self):
        self.username = None
        self.token = None

    wait_time = between(1, 3)
    host = None 
    @task(1)
    def register_or_login(self):
        base_user = "http://toxiproxy:8600"

        if random.random() < 0.5:
            username = f"user_{random_string()}"
            password = "pass123"
            self.client.post(f"{base_user}/register", json={"username": username, "password": password})
        else:
            username = random.choice(["user1", "user2"])
            password = "pass1" if username == "user1" else "pass2"

        self.username = username 

        res = self.client.post(f"{base_user}/login", json={"username": username, "password": password})
        if res.status_code == 200:
            self.token = "valid-token"

    @task(3)
    def browse_products(self):
        base_inventory = "http://toxiproxy:8601"
        self.client.get(f"{base_inventory}/products")

    @task(2)
    def add_product_to_cart(self):
        base_inventory = "http://toxiproxy:8601"
        base_cart = "http://toxiproxy:8602"
        response = self.client.get(f"{base_inventory}/products")
        if response.status_code == 200:
            products = response.json()
            if products:
                product = random.choice(products)
                quantity = random.randint(1, 3)
                self.client.post(f"{base_cart}/cart", json={
                    "product_id": product["product_id"],
                    "quantity": quantity
                })

    @task(1)
    def update_cart_item(self):
        base_cart = "http://toxiproxy:8602"
        response = self.client.get(f"{base_cart}/cart")
        if response.status_code == 200:
            cart_items = response.json()
            if cart_items:
                item = random.choice(cart_items)
                new_quantity = random.randint(1, 5)
                self.client.put(f"{base_cart}/cart/{item['product_id']}", name="/cart/:product_id", params={"quantity": new_quantity})

    @task(1)
    def delete_cart_item(self):
        base_cart = "http://toxiproxy:8602"
        response = self.client.get(f"{base_cart}/cart")
        if response.status_code == 200:
            cart_items = response.json()
            if cart_items:
                item = random.choice(cart_items)
                self.client.delete(f"{base_cart}/cart/{item['product_id']}", name="/cart/:product_id")

    @task(1)
    def place_order(self):
        base_order = "http://toxiproxy:8603"
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.client.post(f"{base_order}/orders", headers=headers)

class AdminUser(HttpUser):
    weight=1
    wait_time = between(1, 3)
    host = None

    def on_start(self):
        self.username = None
        self.token = None
        self.login()

    def login(self):
        base_user = "http://toxiproxy:8600"
        admin_accounts = [
            {"username": "admin1", "password": "adminpass1"},
            {"username": "admin2", "password": "adminpass2"}
        ]
        creds = random.choice(admin_accounts)
        self.username = creds["username"]

        res = self.client.post(f"{base_user}/login", json=creds)
        if res.status_code == 200:
            self.token = "valid-token"

    @task(3)
    def browse_inventory(self):
        base_inventory = "http://toxiproxy:8601"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

        if random.random() < 0.5:
            self.client.get(f"{base_inventory}/products", headers=headers)
        else:
            resp = self.client.get(f"{base_inventory}/products", headers=headers)
            if resp.status_code == 200:
                products = resp.json()
                if products:
                    product = random.choice(products)
                    self.client.get(f"{base_inventory}/products/{product['product_id']}", name="/products/:id", headers=headers)

    @task(2)
    def add_or_update_product(self):
        base_inventory = "http://toxiproxy:8601"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

        if random.random() < 0.1:
            new_product = {
                "product_id": random_string(8),
                "name": f"Product_{random_string(5)}",
                "quantity": random.randint(1, 100)
            }
            self.client.post(f"{base_inventory}/products", json=new_product, headers=headers)
        else:
            resp = self.client.get(f"{base_inventory}/products", headers=headers)
            if resp.status_code == 200:
                products = resp.json()
                if products:
                    product = random.choice(products)
                    qty_change = random.randint(-5, 20)
                    self.client.put(f"{base_inventory}/products/quantity", json={
                        "product_id": product["product_id"],
                        "quantity_change": qty_change
                    }, headers=headers)

    @task(2)
    def browse_orders(self):
        base_order = "http://toxiproxy:8603"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

        if random.random() < 0.5:
            self.client.get(f"{base_order}/orders", headers=headers)
        else:
            resp = self.client.get(f"{base_order}/orders", headers=headers)
            if resp.status_code == 200:
                orders = resp.json()
                if orders:
                    order = random.choice(orders)
                    self.client.get(f"{base_order}/orders/{order['order_id']}", name="/orders/:id", headers=headers)
