class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        value = float(value)
        if value <= 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = value

    def __repr__(self) -> str:
        return f"Ingredient({self.name!r}, {self.quantity}, {self.unit!r})"

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit