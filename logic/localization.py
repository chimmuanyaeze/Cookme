from .models import IngredientManager

class LocalizationService:
    def __init__(self, ingredient_manager: IngredientManager):
        self.ingredient_manager = ingredient_manager

    def localize_ingredient(self, ingredient_id: str, language: str) -> str:
        """
        Returns the localized name of an ingredient.
        """
        return self.ingredient_manager.get_ingredient_name(ingredient_id, language)