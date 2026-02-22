import React from 'react';
import { motion } from 'framer-motion';

const RecipeCard = ({ recipe, onClick }) => {
    // Real image from backend or fallback image
    const imageUrl = recipe.media?.image
        ? `http://localhost:8000/assets/${recipe.media.image}`
        : (recipe.image_url || "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=2656&auto=format&fit=crop");

    return (
        <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onClick(recipe)}
            className="w-32 cursor-pointer flex flex-col items-center"
        >
            <div className="w-full h-24 rounded-2xl overflow-hidden shadow-sm mb-2 border border-stone-200">
                <img
                    src={imageUrl}
                    alt={recipe.title}
                    className="w-full h-full object-cover"
                />
            </div>
            <h3 className="font-serif text-sm text-charcoal text-center leading-tight line-clamp-2 px-1 font-bold italic">
                {recipe.name || recipe.title || 'Unknown Recipe'}
            </h3>
        </motion.div>
    );
};

export default RecipeCard;
