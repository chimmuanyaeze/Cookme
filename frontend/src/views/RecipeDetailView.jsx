import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const RecipeDetailView = ({ recipe, onBack, onStartCooking }) => {
    const [checkedIngredients, setCheckedIngredients] = useState([]);

    if (!recipe) return null;

    // For the UI, let's treat the first 3 ingredients as compulsory, rest as optional if not specified
    const ingredients = recipe.ingredients || [];
    const mappedIngredients = ingredients.map((ing, idx) => ({
        ...ing,
        id: ing.ingredient_id || idx,
        is_optional: ing.is_optional !== undefined ? ing.is_optional : idx >= 3
    }));

    const compulsoryIngredients = mappedIngredients.filter(ing => !ing.is_optional);
    const optionalIngredients = mappedIngredients.filter(ing => ing.is_optional);

    const toggleIngredient = (id) => {
        if (checkedIngredients.includes(id)) {
            setCheckedIngredients(checkedIngredients.filter(itemId => itemId !== id));
        } else {
            setCheckedIngredients([...checkedIngredients, id]);
        }
    };

    const canCook = compulsoryIngredients.every(ing => checkedIngredients.includes(ing.id));

    const handleStartClick = () => {
        if (canCook) {
            // Pass the checked ingredients to the routing layer so we know what's missing
            onStartCooking('transition_splash', { missingOptional: optionalIngredients.filter(ing => !checkedIngredients.includes(ing.id)) });
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="bg-white min-h-screen relative z-30 pb-32"
        >
            {/* Hero Image */}
            <div className="h-72 bg-stone-200 relative overflow-hidden">
                <img
                    src={recipe.media?.image ? `http://localhost:8000/assets/${recipe.media.image}` : (recipe.image_url || "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=2656&auto=format&fit=crop")}
                    alt={recipe.title || "Recipe"}
                    className="w-full h-full object-cover"
                />

                {/* Gradient overlay to make back button visible */}
                <div className="absolute inset-0 bg-gradient-to-b from-black/40 to-transparent h-24 pointer-events-none"></div>

                <button
                    onClick={onBack}
                    className="absolute top-6 left-6 w-10 h-10 rounded-full bg-white/50 backdrop-blur-md flex items-center justify-center text-charcoal shadow-sm z-40 transition-transform active:scale-95"
                >
                    ←
                </button>
            </div>

            <div className="p-8 -mt-6 bg-white rounded-t-[2rem] relative z-40">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <div className="flex justify-between items-start mb-2">
                        <h1 className="text-3xl font-serif text-charcoal pr-4">{recipe.title || recipe.name || 'Delicious Recipe'}</h1>
                        <span className="bg-beige px-3 py-1 rounded-full text-xs font-bold text-stone-600 shrink-0">
                            {recipe.difficulty || 'Medium'}
                        </span>
                    </div>

                    <p className="text-stone-500 text-sm mb-8">
                        {recipe.time || '30m'} • {recipe.serving_size || '2 Servings'}
                    </p>

                    <h3 className="font-bold text-charcoal mb-4 uppercase tracking-wider text-xs">Ingredients</h3>
                    <p className="text-xs text-stone-500 mb-4 italic">Please checkoff compulsory ingredients before starting.</p>

                    {compulsoryIngredients.length > 0 && (
                        <div className="mb-6">
                            <h4 className="text-sm font-medium text-terracotta mb-3">Compulsory <span className="text-stone-400 font-normal text-xs ml-1">(Required)</span></h4>
                            <ul className="space-y-3">
                                {compulsoryIngredients.map((ing) => (
                                    <li
                                        key={ing.id}
                                        onClick={() => toggleIngredient(ing.id)}
                                        className="flex items-center gap-4 text-stone-700 pb-3 border-b border-stone-100 last:border-0 cursor-pointer"
                                    >
                                        <div className={`w-6 h-6 rounded-md border-2 flex items-center justify-center transition-colors ${checkedIngredients.includes(ing.id) ? 'bg-sage border-sage text-white' : 'border-stone-300'}`}>
                                            {checkedIngredients.includes(ing.id) && <span className="text-sm">✓</span>}
                                        </div>
                                        <span className="flex-1 capitalize">{ing.ingredient_id || ing.name || 'Ingredient'}</span>
                                        <span className="font-medium text-stone-900">{ing.quantity} {ing.unit}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {optionalIngredients.length > 0 && (
                        <div>
                            <h4 className="text-sm font-medium text-stone-500 mb-3 mt-6">Optional</h4>
                            <ul className="space-y-3">
                                {optionalIngredients.map((ing) => (
                                    <li
                                        key={ing.id}
                                        onClick={() => toggleIngredient(ing.id)}
                                        className="flex items-center gap-4 text-stone-500 pb-3 border-b border-stone-100 last:border-0 cursor-pointer"
                                    >
                                        <div className={`w-6 h-6 rounded-md border-2 flex items-center justify-center transition-colors ${checkedIngredients.includes(ing.id) ? 'bg-sage border-sage text-white' : 'border-stone-200 bg-stone-50'}`}>
                                            {checkedIngredients.includes(ing.id) && <span className="text-sm">✓</span>}
                                        </div>
                                        <span className="flex-1 capitalize">{ing.ingredient_id || ing.name || 'Ingredient'}</span>
                                        <span className="font-medium">{ing.quantity} {ing.unit}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </motion.div>
            </div>

            {/* Sticky Action Button */}
            <motion.div
                initial={{ y: 100 }}
                animate={{ y: 0 }}
                className="fixed bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-white via-white to-transparent z-50 pointer-events-none"
            >
                <button
                    onClick={handleStartClick}
                    disabled={!canCook}
                    className={`w-full max-w-sm mx-auto block py-4 rounded-2xl font-bold text-lg transition-all pointer-events-auto ${canCook
                        ? 'bg-terracotta text-black shadow-[0_8px_30px_rgba(219,84,65,0.4)] hover:shadow-[0_12px_40px_rgba(219,84,65,0.5)] active:scale-[0.98]'
                        : 'bg-stone-200 text-stone-600 cursor-not-allowed'
                        }`}
                >
                    {canCook ? "Let's Cook" : "Select Required Ingredients"}
                </button>
            </motion.div>
        </motion.div>
    );
};

export default RecipeDetailView;
