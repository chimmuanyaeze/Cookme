import random
from typing import Dict, Optional

class AIService:
    def generate_response(self, prompt: str, context: Dict) -> Dict:
        """
        Generates a response based on the user's prompt and current context.
        Context includes: current_recipe_id, current_step_index.
        Returns: { "text": str, "action": str (optional), "new_context": Dict }
        """
        prompt = prompt.lower()
        recipe = context.get("recipe") # Full recipe object/dict
        step_index = context.get("step_index", 0)
        
        if not recipe:
            # No recipe selected
            if "hello" in prompt:
                return {"text": "Hello! Select a recipe to start cooking.", "new_context": context}
            return {"text": "Please select a recipe first.", "new_context": context}

        steps = recipe.get("steps", [])
        total_steps = len(steps)
        
        # Navigation
        if "next" in prompt or "after" in prompt:
            if step_index + 1 < total_steps:
                next_step = steps[step_index + 1]
                instruction = next_step["instruction"]
                
                # Safety Checks
                danger_keywords = ["cut", "chop", "slice", "knife", "boil", "hot", "fire", "heat", "stove", "oven", "fry", "oil", "blend"]
                safety_warning = ""
                if any(k in instruction.lower() for k in danger_keywords):
                     safety_warning = "⚠️ CAUTION: Be careful! "

                text = f"{safety_warning}Step {next_step['step_number']}: {instruction}"
                
                context["step_index"] = step_index + 1
                return {"text": text, "new_context": context}
            else:
                return {"text": "You are at the last step. Enjoy your meal!", "new_context": context}

        elif "previous" in prompt or "back" in prompt:
            if step_index > 0:
                prev_step = steps[step_index - 1]
                text = f"Going back. Step {prev_step['step_number']}: {prev_step['instruction']}"
                context["step_index"] = step_index - 1
                return {"text": text, "new_context": context}
            else:
                return {"text": "You are at the first step.", "new_context": context}

        elif "repeat" in prompt or "say again" in prompt or "current" in prompt:
            if 0 <= step_index < total_steps:
                step = steps[step_index]
                return {"text": f"Step {step['step_number']}: {step['instruction']}", "new_context": context}
        
        elif "ingredient" in prompt or "shopping" in prompt:
            ingredients = recipe.get("ingredients", [])
            ing_text = ", ".join([f"{i['quantity']} {i['unit']} of {i['ingredient_id']}" for i in ingredients])
            return {"text": f"You need: {ing_text}", "new_context": context}

        elif "timer" in prompt and ("set" in prompt or "start" in prompt):
            import re
            match = re.search(r'(\d+)\s*(minute|min)', prompt)
            minutes = int(match.group(1)) if match else 5
            return {"text": f"Setting a timer for {minutes} minutes.", "action": "set_timer", "timer_minutes": minutes, "new_context": context}

        # Fallback
        return {"text": f"We are on step {step_index + 1}. You can say Next or Repeat.", "new_context": context}

ai_service = AIService()
