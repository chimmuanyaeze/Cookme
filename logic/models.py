from dataclasses import dataclass
from typing import List, Dict, Optional
import json
import os

@dataclass
class Ingredient:
    id: str
    names: Dict[str, str]

    def get_name(self, language: str = "english") -> str:
        return self.names.get(language.lower(), self.names.get("english", self.id))

@dataclass
class RecipeStep:
    step_number: int
    instruction: str
    tip: Optional[str] = None

@dataclass
class RecipeIngredient:
    ingredient_id: str
    quantity: float
    unit: str
    optional: bool = False
    notes: Optional[str] = None

@dataclass
class Recipe:
    id: str
    name: str
    origin: Dict[str, str]
    category: str
    difficulty: str
    estimated_time_minutes: int
    serving_size: str
    ingredients: List[RecipeIngredient]
    steps: List[RecipeStep]
    media: Dict[str, str]

class IngredientManager:
    def __init__(self, filepath: str):
        self.ingredients: Dict[str, Ingredient] = {}
        self.load_ingredients(filepath)

    def load_ingredients(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Ingredients file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get("ingredients", []):
                self.ingredients[item["id"]] = Ingredient(id=item["id"], names=item["names"])

    def get_ingredient(self, ingredient_id: str) -> Optional[Ingredient]:
        return self.ingredients.get(ingredient_id)

    def get_ingredient_name(self, ingredient_id: str, language: str) -> str:
        ingredient = self.get_ingredient(ingredient_id)
        if ingredient:
            return ingredient.get_name(language)
        return ingredient_id

class RecipeManager:
    def __init__(self, filepath: str):
        self.recipes: Dict[str, Recipe] = {}
        self.load_recipes(filepath)

    def load_recipes(self, filepath: str):
         if not os.path.exists(filepath):
            raise FileNotFoundError(f"Recipes file not found: {filepath}")

         with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get("recipes", []):
                ingredients = [RecipeIngredient(**ing) for ing in item.get("ingredients", [])]
                steps = [RecipeStep(**step) for step in item.get("steps", [])]
                
                self.recipes[item["id"]] = Recipe(
                    id=item["id"],
                    name=item["name"],
                    origin=item["origin"],
                    category=item["category"],
                    difficulty=item["difficulty"],
                    estimated_time_minutes=item["estimated_time_minutes"],
                    serving_size=item.get("serving_size", "4 people"),
                    ingredients=ingredients,
                    steps=steps,
                    media=item.get("media", {})
                )

    def get_all_recipes(self) -> List[Recipe]:
        return list(self.recipes.values())

    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        return self.recipes.get(recipe_id)
