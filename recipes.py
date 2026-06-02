class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __repr__(self):
        return f"Ingredient({self.name!r}, {self.quantity}, {self.unit!r})"

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __eq__(self, other: object):
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

    def add_ingredient(self, ingredient: Ingredient):
        for reality_ingredient in self.ingredients:
            if reality_ingredient == ingredient:
                reality_ingredient.quantity += ingredient.quantity
                return
        self.ingredients.append(
            Ingredient(ingredient.name, ingredient.quantity, ingredient.unit)
        )

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, Real) and ratio > 0

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")
        scaled_ingredients = [Ingredient(ingredient.name, ingredient.quantity * ratio,ingredient.unit,) for ingredient in self.ingredients]
        return Recipe(self.title, scaled_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients_text = "\n".join(str(ingredient) for ingredient in self.ingredients)
        if not ingredients_text:
            return self.title
        return f"{self.title}\n{ingredients_text}"

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        total_quantities = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            total_quantities[key] = total_quantities.get(key, 0) + ingredient.quantity
        shopping_items = [Ingredient(name, quantity, unit) for (name, unit), quantity in total_quantities.items()]
        return sorted(shopping_items, key=lambda ingredient: ingredient.name)

    def __add__(self, other: "ShoppingList"):
        comb = ShoppingList()
        for ingredient, recipe_title in self._items + other._items:
            comb._items.append((Ingredient(ingredient.name,ingredient.quantity,ingredient.unit,),recipe_title,))
        return comb