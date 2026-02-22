import React from 'react';
import { motion } from 'framer-motion';

const SavedView = () => {
    return (
        <div className="pt-24 pb-32 px-6 max-w-md mx-auto min-h-screen">
            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-3xl font-serif text-charcoal mb-8"
            >
                Saved Recipes
            </motion.h1>
            <div className="flex flex-col items-center justify-center mt-20 text-center text-stone-400">
                <span className="text-6xl mb-4">🧊</span>
                <p>Saved recipes will appear here.</p>
            </div>
        </div>
    );
};

export default SavedView;
