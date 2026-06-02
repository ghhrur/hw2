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
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __repr__(self) -> str:
        return f"Ingredient({self.name!r}, {self.quantity}, {self.unit!r})"

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title: str, ingredients: list[Ingredient] | None = None):
        self.title = title
        self.ingredients = []
        if ingredients is not None:
            for ingredient in ingredients:
                self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient: Ingredient) -> None:
        for reality_ingredient in self.ingredients:
            if reality_ingredient == ingredient:
                reality_ingredient.quantity += ingredient.quantity
                return
        self.ingredients.append(
            Ingredient(ingredient.name, ingredient.quantity, ingredient.unit)
        )

    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        return isinstance(ratio, Real) and ratio > 0

    def scale(self, ratio: float) -> "Recipe":
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")
        scaled_ingredients = [Ingredient(ingredient.name, ingredient.quantity * ratio,ingredient.unit,) for ingredient in self.ingredients]
        return Recipe(self.title, scaled_ingredients)

    def __len__(self) -> int:
        return len(self.ingredients)

    def __str__(self) -> str:
        ingredients_text = "\n".join(str(ingredient) for ingredient in self.ingredients)
        if not ingredients_text:
            return self.title
        return f"{self.title}\n{ingredients_text}"