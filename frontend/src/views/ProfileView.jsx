import React from 'react';
import { motion } from 'framer-motion';

const ProfileView = () => {
    // Mock user data
    const userStats = {
        rank: 'Noob Chef',
        cookedCount: 0,
        dailyStreak: 0,
        longestStreak: 0,
    };

    return (
        <div className="pt-24 pb-32 px-6 max-w-md mx-auto min-h-screen bg-stone-50">
            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-3xl font-serif text-charcoal mb-8 text-center"
            >
                Profile
            </motion.h1>

            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="bg-white rounded-3xl p-6 shadow-sm mb-6"
            >
                <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 bg-stone-200 rounded-full flex items-center justify-center text-3xl">
                        👤
                    </div>
                    <div>
                        <h2 className="text-xl font-medium text-charcoal">Chef User</h2>
                        <p className="text-stone-500 text-sm">user@example.com</p>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="bg-stone-50 p-4 rounded-2xl text-center">
                        <span className="block text-2xl font-serif text-terracotta mb-1">{userStats.rank}</span>
                        <span className="text-xs text-stone-500 uppercase tracking-widest">Current Rank</span>
                    </div>
                    <div className="bg-stone-50 p-4 rounded-2xl text-center">
                        <span className="block text-2xl font-serif text-charcoal mb-1">{userStats.cookedCount}</span>
                        <span className="text-xs text-stone-500 uppercase tracking-widest">Recipes Cooked</span>
                    </div>
                    <div className="bg-stone-50 p-4 rounded-2xl text-center">
                        <span className="block text-2xl font-serif text-sage mb-1">{userStats.dailyStreak}🔥</span>
                        <span className="text-xs text-stone-500 uppercase tracking-widest">Daily Streak</span>
                    </div>
                    <div className="bg-stone-50 p-4 rounded-2xl text-center">
                        <span className="block text-2xl font-serif text-charcoal mb-1">{userStats.longestStreak}</span>
                        <span className="text-xs text-stone-500 uppercase tracking-widest">Best Streak</span>
                    </div>
                </div>
            </motion.div>

            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="space-y-4"
            >
                {['Activities', 'Liked Recipes', 'Disliked Recipes', 'Security'].map((item) => (
                    <button key={item} className="w-full bg-white px-6 py-4 rounded-2xl text-left font-medium text-charcoal shadow-sm flex justify-between items-center hover:bg-stone-50 transition-colors">
                        {item}
                        <span className="text-stone-300">→</span>
                    </button>
                ))}
            </motion.div>
        </div>
    );
};

export default ProfileView;
