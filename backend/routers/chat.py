from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Mock Database
RECIPES = [
    {
        "id": "egusi_soup",
        "name": "Egusi Soup",
        "description": "A rich, savory Nigerian stew made with ground melon seeds and spinach.",
        "difficulty": "Medium",
        "category": "Dinner",
        "estimated_time_minutes": 45,
        "serving_size": "4 servings",
        "media": {
            "image": "egusi_soup.jpg" # Placeholder
        },
        "ingredients": [
            {"ingredient_id": "Ground Egusi", "quantity": 2, "unit": "cups"},
            {"ingredient_id": "Palm Oil", "quantity": 1, "unit": "cup"},
            {"ingredient_id": "Beef/Goat Meat", "quantity": 500, "unit": "g"},
            {"ingredient_id": "Spinach", "quantity": 1, "unit": "bunch"}
        ],
        "steps": [
            {"step_number": 1, "instruction": "Boil the meat with onions and seasoning until tender.", "tip": "Use a pressure cooker to save time!"},
            {"step_number": 2, "instruction": "In a separate pot, heat the palm oil and add the ground egusi mixed with a little water.", "tip": "Stir constantly to prevent burning."},
            {"step_number": 3, "instruction": "Add the meat stock and let it simmer for 15 minutes.", "tip": None},
            {"step_number": 4, "instruction": "Add the spinach and cooked meat. Simmer for another 5 minutes.", "tip": "Don't overcook the vegetables."}
        ]
    },
    {
        "id": "jollof_rice",
        "name": "Jollof Rice",
        "description": "The classic West African spiced rice dish.",
        "difficulty": "Hard",
        "category": "Lunch",
        "estimated_time_minutes": 60,
        "serving_size": "6 servings",
        "media": {
            "image": "jollof_rice.jpg"
        },
        "ingredients": [
             {"ingredient_id": "Long Grain Rice", "quantity": 3, "unit": "cups"},
             {"ingredient_id": "Tomato Paste", "quantity": 1, "unit": "cup"}
        ],
        "steps": [
            {"step_number": 1, "instruction": "Parboil the rice and wash thoroughly.", "tip": "Removes excess starch."}
        ]
    }
]

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = {}

@router.get("/recipes")
async def get_recipes():
    return RECIPES

@router.post("/chat")
async def chat_interaction(request: ChatRequest):
    # Simple Mock Response for now
    return {
        "text": f"I received your command: {request.message}. (Backend is running!)",
        "audio_url": None,
        "new_context": request.context
    }
