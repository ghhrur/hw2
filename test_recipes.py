import pytest

from recipes import DietaryRecipe, Ingredient, Recipe, ShoppingList
def test_ingredient_creator():
    ingredient = Ingredient("Сахар", 100, "г")

    assert ingredient.name == "Сахар"
    assert ingredient.quantity == 100.0
    assert ingredient.unit == "г"

def test_ingredient_str():
    ingredient = Ingredient("Сахар", 100, "г")
    assert str(ingredient) == "Сахар: 100.0 г"

def test_ingredient_uses_name_and_unit_for_equality():
    assert Ingredient("Сахар", 100, "г") == Ingredient("Сахар", 200, "г")
    assert Ingredient("Сахар", 100, "г") != Ingredient("Соль", 100, "г")
    assert Ingredient("Сахар", 100, "г") != Ingredient("Сахар", 1, "кг")

def test_ingredient_quantity_tobe_positive():
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Сахар", 0, "г")

def test_recipe_creation():
    ingredients = [Ingredient("Яйцо", 2, "шт"), Ingredient("Молоко", 100, "мл")]
    recipe = Recipe("Омлет", ingredients)
    assert recipe.title == "Омлет"
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[0] == Ingredient("Яйцо", 1, "шт")
    assert recipe.ingredients[1] == Ingredient("Молоко", 1, "мл")

def test_recipe_add_new_ingredient():
    recipe = Recipe("Омлет")
    recipe.add_ingredient(Ingredient("Соль", 5, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0] == Ingredient("Соль", 1, "г")

def test_recipe_add_real_ingredient():
    recipe = Recipe("Омлет", [Ingredient("Яйцо", 2, "шт")])
    recipe.add_ingredient(Ingredient("Яйцо", 1, "шт"))
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 3.0

def test_recipe_scale_returns_new_and_original():
    recipe = Recipe("Омлет",[Ingredient("Яйцо", 2, "шт"), Ingredient("Молоко", 100, "мл")])
    scaled_recipe = recipe.scale(3)
    assert isinstance(scaled_recipe, Recipe)
    assert scaled_recipe is not recipe
    assert scaled_recipe.ingredients[0].quantity == 6.0
    assert scaled_recipe.ingredients[1].quantity == 300.0
    assert recipe.ingredients[0].quantity == 2.0
    assert recipe.ingredients[1].quantity == 100.0

def test_recipe_scale_decline_novalid_ratio():
    recipe = Recipe("Омлет", [Ingredient("Яйцо", 2, "шт")])
    with pytest.raises(ValueError, match="Коэффициент должен быть положительным"):
        recipe.scale(0)

def test_recipe_counts_unique_ingredients():
    recipe = Recipe("Омлет",[Ingredient("Яйцо", 2, "шт"),Ingredient("Яйцо", 1, "шт"),Ingredient("Молоко", 100, "мл")])
    assert len(recipe) == 2
    assert recipe.ingredients[0].quantity == 3.0

def test_dietary_recipe_scale_diet_type():
    recipe = DietaryRecipe("Овощной салат","веган",[Ingredient("Огурец", 2, "шт")])
    scaled_recipe = recipe.scale(2)
    assert isinstance(scaled_recipe, DietaryRecipe)
    assert scaled_recipe.diet_type == "веган"
    assert scaled_recipe.ingredients[0] == Ingredient("Огурец", 1, "шт")
    assert scaled_recipe.ingredients[0].quantity == 4.0

def test_dietary_recipe_str_adds_diet_type():
    recipe = DietaryRecipe("Овощной салат","веган", [Ingredient("Огурец", 2, "шт")])
    assert str(recipe).startswith("[веган] Овощной салат")

def test_shopping_list_add_recipe():
    recipe = Recipe("Паста", [Ingredient("Макароны", 300, "г")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    items = shopping_list.get_list()
    assert len(items) == 1
    assert items[0] == Ingredient("Макароны", 1, "г")
    assert items[0].quantity == 600.0

def test_shopping_list_add_recipe_declines_novalid_portions():
    recipe = Recipe("Паста", [Ingredient("Макароны", 300, "г")])
    shopping_list = ShoppingList()
    with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
        shopping_list.add_recipe(recipe, 0)

def test_shopping_list_remove_recipe():
    pasta = Recipe("Паста", [Ingredient("Макароны", 300, "г")])
    sauce = Recipe("Соус", [Ingredient("Томаты", 200, "г")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pasta, 1)
    shopping_list.add_recipe(sauce, 1)
    shopping_list.remove_recipe("Паста")
    items = shopping_list.get_list()
    assert len(items) == 1
    assert items[0] == Ingredient("Томаты", 1, "г")
    assert items[0].quantity == 200.0

def test_shopping_list_remove_imaginary_recipe():
    recipe = Recipe("Паста", [Ingredient("Макароны", 300, "г")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    shopping_list.remove_recipe("Несуществующий рецепт")
    items = shopping_list.get_list()
    assert len(items) == 1
    assert items[0] == Ingredient("Макароны", 1, "г")
    assert items[0].quantity == 300.0

def test_shopping_list_get_sums_sorts_ingredients():
    pasta = Recipe("Паста",[Ingredient("Макароны", 300, "г"), Ingredient("Сыр", 100, "г")])
    salad = Recipe("Салат",[Ingredient("Огурец", 2, "шт"), Ingredient("Сыр", 50, "г")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pasta, 1)
    shopping_list.add_recipe(salad, 2)
    items = shopping_list.get_list()
    assert [ingredient.name for ingredient in items] == ["Макароны", "Огурец", "Сыр"]
    assert items[0].quantity == 300.0
    assert items[1].quantity == 4.0
    assert items[2].quantity == 200.0

def test_shopping_list_add_combo_without_change_orig():
    pasta = Recipe("Паста", [Ingredient("Макароны", 300, "г")])
    sauce = Recipe("Соус", [Ingredient("Томаты", 200, "г")])
    first_list = ShoppingList()
    second_list = ShoppingList()
    first_list.add_recipe(pasta, 1)
    second_list.add_recipe(sauce, 2)
    combined_list = first_list + second_list
    combined_items = combined_list.get_list()
    assert [ingredient.name for ingredient in combined_items] == ["Макароны", "Томаты"]
    assert combined_items[0].quantity == 300.0
    assert combined_items[1].quantity == 400.0
    assert len(first_list.get_list()) == 1
    assert len(second_list.get_list()) == 1