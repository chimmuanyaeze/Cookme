
import unittest
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.real_services import RuleBasedAIService
from logic.models import Recipe, RecipeIngredient, RecipeStep

class TestContextAwareAI(unittest.TestCase):
    def setUp(self):
        self.ai = RuleBasedAIService()
        
        # Create Dummy Recipe
        self.ingredients = [
            RecipeIngredient("rice", 2, "cups"),
            RecipeIngredient("tomato", 4, "pieces")
        ]
        self.steps = [
            RecipeStep(1, "Wash the rice.", "Use cold water"),
            RecipeStep(2, "Boil the water.", "Add salt"),
            RecipeStep(3, "Add rice to boiling water.", None)
        ]
        self.recipe = Recipe(
            id="test-recipe",
            name="Test Rice",
            origin={},
            category="Test",
            difficulty="Easy",
            estimated_time_minutes=30,
            ingredients=self.ingredients,
            steps=self.steps,
            media={}
        )

    def test_ingredients_query(self):
        context = {"recipe": self.recipe, "step_index": 0}
        response = self.ai.generate_response("what are the ingredients?", context)
        self.assertIn("rice", response)
        self.assertIn("tomato", response)
        self.assertIn("You need:", response)

    def test_first_step_query(self):
        context = {"recipe": self.recipe, "step_index": 0}
        # "current step" or just asking what to do
        response = self.ai.generate_response("what is the current step?", context)
        self.assertIn("Wash the rice", response)

    def test_next_step_logic(self):
        # Current step is 0 (Wash rice). User says "next". Should read Step 1 (Boil water).
        context = {"recipe": self.recipe, "step_index": 0}
        response = self.ai.generate_response("next step", context)
        self.assertIn("Boil the water", response)

    def test_next_step_at_end(self):
        # Current step is 2 (Add rice). User says "next".
        context = {"recipe": self.recipe, "step_index": 2}
        response = self.ai.generate_response("next step", context)
        self.assertIn("last step", response)

    def test_previous_step(self):
        # Current step is 1 (Boil water). User says "previous". Should read Step 0 (Wash rice).
        context = {"recipe": self.recipe, "step_index": 1}
        response = self.ai.generate_response("go back", context)
        self.assertIn("Wash the rice", response)

    def test_no_context(self):
        response = self.ai.generate_response("hello")
        self.assertIn("Please select a recipe", response)

if __name__ == '__main__':
    unittest.main()
