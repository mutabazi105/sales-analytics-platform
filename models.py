"""
Object-Oriented Data Models for Sales Analytics Platform
"""
from abc import ABC, abstractmethod


class Entity(ABC):
    """Base class for all entities"""

    def __init__(self, entity_id: str, name: str):
        self._validate_id(entity_id)
        self._validate_name(name)
        self.id = entity_id
        self.name = name

    def _validate_id(self, entity_id):
        if not entity_id or not isinstance(entity_id, str):
            raise ValueError("ID must be a non-empty string")

    def _validate_name(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

    @abstractmethod
    def to_dict(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} (ID: {self.id})"

    def __repr__(self):
        return f"{self.__class__.__name__}(id='{self.id}', name='{self.name}')"


class Product(Entity):
    """Product entity with category and pricing"""

    def __init__(self, product_id: str, name: str, category: str, base_price: float):
        super().__init__(product_id, name)
        self.category = category
        self.base_price = base_price
        self._validate_price()

    def _validate_price(self):
        if self.base_price < 0:
            raise ValueError("Price cannot be negative")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "base_price": self.base_price
        }

    def __str__(self):
        return f"Product: {self.name} - ${self.base_price:.2f} ({self.category})"

    def __repr__(self):
        return f"Product(id='{self.id}', name='{self.name}', category='{self.category}', base_price={self.base_price})"


class Customer(Entity):
    """Customer entity with contact information"""

    def __init__(self, customer_id: str, name: str, email: str, lifetime_value: float = 0.0):
        super().__init__(customer_id, name)
        self.email = email
        self.lifetime_value = lifetime_value
        self.orders = []
        self._validate_email()

    def _validate_email(self):
        if "@" not in self.email:
            raise ValueError("Invalid email format")

    def update_lifetime_value(self, amount: float):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.lifetime_value += amount

    def add_order(self, order):
        self.orders.append(order)
        if order.status == "completed":
            self.update_lifetime_value(order.amount)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "lifetime_value": self.lifetime_value,
            "order_count": len(self.orders)
        }

    def __str__(self):
        return f"Customer: {self.name} (LTV: ${self.lifetime_value:.2f})"

    def __repr__(self):
        return f"Customer(id='{self.id}', name='{self.name}', email='{self.email}', lifetime_value={self.lifetime_value})"


class Order:
    """Order entity representing a sales transaction"""

    VALID_STATUSES = ["pending", "completed", "cancelled"]

    def __init__(self, order_id: str, date: str, customer: Customer,
                 items: list, amount: float, status: str = "pending"):
        self.order_id = order_id
        self.date = date
        self.customer = customer
        self.items = items
        self.amount = amount
        self.status = status
        self._validate_status()

    def _validate_status(self):
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {self.VALID_STATUSES}")

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "date": self.date,
            "customer_id": self.customer.id,
            "item_count": len(self.items),
            "amount": self.amount,
            "status": self.status
        }

    def __str__(self):
        return f"Order {self.order_id}: ${self.amount:.2f} ({self.status})"

    def __repr__(self):
        return f"Order(order_id='{self.order_id}', amount={self.amount}, status='{self.status}')"


class EntityFactory:
    """Factory for creating entities"""

    @staticmethod
    def create_product_from_row(row):
        return Product(
            product_id=row.get('product_name', ''),
            name=row.get('product_name', 'Unknown'),
            category=row.get('product_category', 'Uncategorized'),
            base_price=float(row.get('unit_price', 0))
        )

    @staticmethod
    def create_customer_from_row(row):
        return Customer(
            customer_id=row.get('customer_id', ''),
            name=f"Customer_{row.get('customer_id', 'Unknown')}",
            email=f"customer_{row.get('customer_id', 'unknown')}@example.com"
        )
