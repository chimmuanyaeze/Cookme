import React from 'react';
import { motion } from 'framer-motion';

const CookedView = ({ onStartCooking }) => {
    // Mock empty state for now
    const cookedRecipes = [];

    return (
        <div className="pt-24 pb-32 px-6 max-w-md mx-auto min-h-screen">
            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-3xl font-serif text-charcoal mb-8"
            >
                Cooked Recipes
            </motion.h1>

            {cookedRecipes.length === 0 ? (
                <div className="flex flex-col items-center justify-center mt-20 text-center">
                    <span className="text-6xl mb-6">👨‍🍳</span>
                    <p className="text-stone-500 mb-8 font-medium">We haven't cooked anything yet</p>
                    <button
                        onClick={onStartCooking}
                        className="px-8 py-4 rounded-full bg-terracotta text-stone-900 font-bold shadow-md hover:shadow-lg transition-all"
                    >
                        Let's start cooking!
                    </button>
                </div>
            ) : (
                <div className="space-y-4">
                    {/* List will go here later */}
                </div>
            )}
        </div>
    );
};

export default CookedView;
