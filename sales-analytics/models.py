from abc import ABC
from typing import Dict, Any
from datetime import datetime

# 1) Object-Oriented Data Models
# Define classes to represent your domain:
# • Product: id, name, category, base price
# • Customer: id, name, email, lifetime value
# • Order: date, items, customer, amount, status
# • SalesAnalyzer: orchestrates loading, cleaning, and analysis


class Entity(ABC):
    """
    its gonna provide common functionality for id management etc.

    attributes:
        _id: unique identifier for the entity
    """

    def __init__(self, entity_id):
        if not entity_id or not str(entity_id).strip():
            raise ValueError("Entity ID cannot be empty or whitespace.")
        self._id = str(entity_id).strip()

    @property
    def id(self) -> str:
        """Get the entity's unique identifier."""
        return self._id


class Product(Entity):
    """It's a product in the sales system

    Args:
        product_id (str): Unique identifier for the product
        name (str): Name of the product
        category (str): Category of the product
        base_price (float): Base price of the product
    """

    def __init__(self, product_id: str, name: str, category: str, base_price: float):
        super().__init__(product_id)

        if not name or not str(name).strip():
            raise ValueError("Product name cannot be empty")
        if not category or not str(category).strip():
            raise ValueError("Product category cannot be empty")
        if base_price is None or base_price < 0:
            raise ValueError("Base price must be a non-negative number")

        self._name = str(name).strip()
        self._category = str(category).strip()
        self._base_price = float(base_price)

    @property
    def name(self) -> str:
        """Get product name."""
        return self._name

    @property
    def category(self) -> str:
        """Get product category."""
        return self._category

    @property
    def base_price(self) -> float:
        """Get product base price."""
        return self._base_price


class Customer(Entity):
    """TODO: explain even though its pretty self-explanatory"""

    def __init__(self, customer_id: str, name: str, email: str, lifetime_value: float):
        super().__init__(customer_id)

        if not name or not str(name).strip():
            raise ValueError("Customer name cannot be empty")
        if not email or not str(email).strip():
            raise ValueError("Customer email cannot be empty")
        if lifetime_value is None or lifetime_value < 0:
            raise ValueError("Lifetime value must be a non-negative number")

        self._name = str(name).strip()
        self._email = str(email).strip()
        self._lifetime_value = float(lifetime_value)

    @property
    def name(self) -> str:
        """Get customer name."""
        return self._name

    @property
    def email(self) -> str:
        """Get customer email."""
        return self._email

    @property
    def lifetime_value(self) -> float:
        """Get customer lifetime value."""
        return self._lifetime_value

    def add_purchase(self, amount: float) -> None:
        """
        Add a purchase amount to lifetime value.

        Args:
            amount: Purchase amount to add
        """
        if amount > 0:
            self._lifetime_value += amount

    def to_dict(self) -> Dict[str, Any]:
        """Convert customer to a dictionary."""
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "lifetime_value": self._lifetime_value,
        }


class Order(Entity):
    """
    Represents a sales order in the system.

    Attributes:
        date: Order date
        customer_id: ID of the customer who placed the order
        product_name: Name of the product ordered
        product_category: Category of the product
        quantity: Number of items ordered
        unit_price: Price per unit
        amount: Total order amount
        status: Order status (completed, pending, cancelled)
    """

    VALID_STATUSES = {"completed", "pending", "cancelled"}

    def __init__(
        self,
        order_id: str,
        date: datetime,
        customer_id: str,
        product_name: str,
        product_category: str,
        quantity: int,
        unit_price: float,
        amount: float,
        status: str = "pending",
    ):
        """
        Initialize an Order.

        Args:
            order_id: Unique order identifier
            date: Order date
            customer_id: Customer ID
            product_name: Product name
            product_category: Product category
            quantity: Order quantity
            unit_price: Price per unit
            amount: Total order amount
            status: Order status

        Raises:
            ValueError: If validation fails for any field
        """
        super().__init__(order_id)

        if not isinstance(date, datetime):
            raise ValueError("Order date must be a datetime object")
        if not customer_id:
            raise ValueError("Customer ID cannot be empty")
        if quantity is None or int(quantity) < 1:
            raise ValueError("Quantity must be at least 1")
        if unit_price is None or float(unit_price) < 0:
            raise ValueError("Unit price cannot be negative")
        if amount is None or float(amount) < 0:
            raise ValueError("Amount cannot be negative")

        # Normalize status
        status_normalized = str(status).lower().strip() if status else "pending"
        if status_normalized not in self.VALID_STATUSES:
            status_normalized = "pending"

        self._date = date
        self._customer_id = str(customer_id).strip()
        self._product_name = str(product_name).strip()
        self._product_category = str(product_category).strip()
        self._quantity = int(quantity)
        self._unit_price = float(unit_price)
        self._amount = float(amount)
        self._status = status_normalized

    @property
    def date(self) -> datetime:
        """Get order date."""
        return self._date

    @property
    def customer_id(self) -> str:
        """Get customer ID."""
        return self._customer_id

    @property
    def product_name(self) -> str:
        """Get product name."""
        return self._product_name

    @property
    def product_category(self) -> str:
        """Get product category."""
        return self._product_category

    @property
    def quantity(self) -> int:
        """Get order quantity."""
        return self._quantity

    @property
    def unit_price(self) -> float:
        """Get unit price."""
        return self._unit_price

    @property
    def amount(self) -> float:
        """Get total order amount."""
        return self._amount

    @property
    def status(self) -> str:
        """Get order status."""
        return self._status

    @property
    def is_completed(self) -> bool:
        """Check if order is completed."""
        return self._status == "completed"

    def to_dict(self) -> Dict[str, Any]:
        """Convert order to dictionary."""
        return {
            "id": self._id,
            "date": self._date.isoformat(),
            "customer_id": self._customer_id,
            "product_name": self._product_name,
            "product_category": self._product_category,
            "quantity": self._quantity,
            "unit_price": self._unit_price,
            "amount": self._amount,
            "status": self._status,
        }


class EntityFactory:
    """
    Factory class for creating domain entities.

    Implements the Factory design pattern to centralize entity creation
    and provide a consistent interface for object instantiation.
    """

    @staticmethod
    def create_product(data: Dict[str, Any]) -> Product:
        """
        Create a Product from dictionary data.

        Args:
            data: Dictionary with product attributes

        Returns:
            Product instance
        """
        return Product(
            product_id=data.get("id", data.get("product_id", "")),
            name=data.get("name", data.get("product_name", "")),
            category=data.get("category", data.get("product_category", "")),
            base_price=float(data.get("base_price", data.get("unit_price", 0))),
        )

    @staticmethod
    def create_customer(data: Dict[str, Any]) -> Customer:
        """
        Create a Customer from dictionary data.

        Args:
            data: Dictionary with customer attributes

        Returns:
            Customer instance
        """
        return Customer(
            customer_id=data.get("id", data.get("customer_id", "")),
            name=data.get(
                "name",
                data.get(
                    "customer_name", f"Customer {data.get('customer_id', 'Unknown')}"
                ),
            ),
            email=data.get("email"),
            lifetime_value=float(data.get("lifetime_value", 0)),
        )

    @staticmethod
    def create_order(data: Dict[str, Any], date_parser=None) -> Order:
        """
        Create an Order from dictionary data.

        Args:
            data: Dictionary with order attributes
            date_parser: Optional function to parse dates

        Returns:
            Order instance
        """
        from utils import parse_date

        order_date = data.get("date", data.get("order_date"))
        if isinstance(order_date, str):
            order_date = parse_date(order_date) or datetime.now()
        elif not isinstance(order_date, datetime):
            order_date = datetime.now()

        return Order(
            order_id=data.get("id", data.get("order_id", "")),
            date=order_date,
            customer_id=data.get("customer_id", ""),
            product_name=data.get("product_name", ""),
            product_category=data.get("product_category", data.get("category", "")),
            quantity=int(data.get("quantity", 1)),
            unit_price=float(data.get("unit_price", 0)),
            amount=float(data.get("amount", data.get("order_amount", 0))),
            status=data.get("status", "pending"),
        )
