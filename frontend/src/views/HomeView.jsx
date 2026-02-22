import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import RecipeCard from '../components/RecipeCard';

const HomeView = ({ onSelectRecipe }) => {
    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        // Fetch recipes from backend
        fetch('http://localhost:8000/api/chat/recipes')
            .then(res => res.json())
            .then(data => setRecipes(data))
            .catch(err => console.error(err));
    }, []);

    // Helper to generate horizontal list sections
    const renderRecipeSection = (title, items) => {
        if (!items || items.length === 0) return null;
        return (
            <div className="mb-6">
                <h2 className="text-stone-500 font-serif text-lg mb-3 px-6 italic">{title}</h2>
                <div className="flex overflow-x-auto hide-scrollbar px-6 gap-4 pb-2 snap-x">
                    {items.map((recipe, index) => (
                        <div key={recipe.id || index} className="snap-start shrink-0">
                            <RecipeCard recipe={recipe} onClick={onSelectRecipe} />
                        </div>
                    ))}
                </div>
            </div>
        );
    };

    // For demonstration, let's use the fetched recipes for all categories
    // In a real app, these would be distinct API calls or filtered lists
    const lastCooked = recipes.slice(0, 3);
    const recommended = recipes.slice(1, 4);
    const mostPopular = recipes.slice(0, 5);

    return (
        <div className="pt-12 min-h-screen">
            <div className="px-6 flex justify-between items-center mb-6">
                <motion.h1
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="text-4xl font-serif text-charcoal italic font-bold"
                >
                    Home
                </motion.h1>
                <div className="w-10 h-10 rounded-full border-2 border-charcoal flex items-center justify-center text-xl cursor-pointer">
                    👤
                </div>
            </div>

            {/* Hero Image */}
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="px-6 mb-8"
            >
                <div className="w-full h-48 rounded-[2rem] overflow-hidden shadow-lg relative">
                    <img
                        src="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=2642&auto=format&fit=crop"
                        alt="Cooking Fire"
                        className="w-full h-full object-cover"
                    />
                </div>
            </motion.div>

            {/* Sections */}
            {recipes.length > 0 ? (
                <>
                    {renderRecipeSection('Last-Cooked', lastCooked)}
                    {renderRecipeSection('Recommended', recommended)}
                    {renderRecipeSection('Most Popular', mostPopular)}
                </>
            ) : (
                <div className="px-6 text-center text-stone-400 mt-12">
                    Loading recipes...
                </div>
            )}

            <style jsx>{`
                .hide-scrollbar::-webkit-scrollbar {
                    display: none;
                }
                .hide-scrollbar {
                    -ms-overflow-style: none;
                    scrollbar-width: none;
                }
            `}</style>
        </div>
    );
};

export default HomeView;
