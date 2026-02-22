from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.services.recipe_manager import recipe_manager
from backend.services.ai import ai_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    context: Dict[str, Any] = {} 
    # Context should contain: 'recipe_id', 'step_index'

@router.get("/recipes")
def get_recipes():
    return recipe_manager.get_all_recipes()

@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: str):
    recipe = recipe_manager.get_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.post("/chat")
def chat(request: ChatRequest):
    message = request.message
    context = request.context
    
    # Hydrate context with full recipe if only ID is present
    recipe_id = context.get("recipe_id")
    if recipe_id and not context.get("recipe"):
        recipe = recipe_manager.get_recipe_by_id(recipe_id)
        if recipe:
            context["recipe"] = recipe
    
    response = ai_service.generate_response(message, context)
    
    # Remove heavy recipe object from response context to save bandwidth, 
    # frontend should keep state or we rely on ID.
    # Actually, for stateless API, we might need to send back what's needed.
    # But let's just send back indices and IDs.
    new_context = response.get("new_context", {})
    if "recipe" in new_context:
        del new_context["recipe"] # Don't send full DB back and forth
        
    response["new_context"] = new_context
    return response
