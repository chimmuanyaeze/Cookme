import json
import os
from typing import List, Optional, Dict

class RecipeManager:
    def __init__(self, data_path: str = "backend/data/recipes/recipes.json"):
        # Adjust path if running from root
        if not os.path.exists(data_path):
             # Fallback for different CWD
             data_path = "data/recipes/recipes.json"
        
        self.data_path = data_path
        self.recipes: List[Dict] = []
        self.load_recipes()

    def load_recipes(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.recipes = data.get("recipes", [])
        except Exception as e:
            print(f"Error loading recipes: {e}")
            self.recipes = []

    def get_all_recipes(self) -> List[Dict]:
        """Returns a list of all recipes (summarized)."""
        return self.recipes

    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict]:
        for recipe in self.recipes:
            if recipe["id"] == recipe_id:
                return recipe
        return None

# Global instance
recipe_manager = RecipeManager()
