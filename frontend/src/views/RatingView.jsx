import React, { useState } from 'react';
import { motion } from 'framer-motion';

const RatingView = ({ onComplete }) => {
    const [outcomeRating, setOutcomeRating] = useState(0);
    const [helpfulnessRating, setHelpfulnessRating] = useState(0);
    const [feedback, setFeedback] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // In a real app, submit this data to backend
        console.log({ outcomeRating, helpfulnessRating, feedback });
        onComplete();
    };

    const renderStars = (rating, setRating) => {
        return (
            <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map(star => (
                    <motion.button
                        key={star}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => setRating(star)}
                        type="button"
                        className={`text-4xl transition-colors ${rating >= star ? 'text-sage' : 'text-stone-200 grayscale'}`}
                    >
                        ⭐
                    </motion.button>
                ))}
            </div>
        );
    };

    return (
        <div className="fixed inset-0 z-50 bg-beige flex flex-col p-6 overflow-y-auto">
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-md mx-auto w-full pt-12 pb-24"
            >
                <div className="text-center mb-10">
                    <span className="text-6xl block mb-4">🏆</span>
                    <h1 className="text-3xl font-serif text-charcoal mb-2">Cooking Complete!</h1>
                    <p className="text-stone-500">Your culinary masterpiece is ready.</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-8 bg-white p-6 rounded-3xl shadow-sm border border-stone-100">

                    {/* Outcome Rating */}
                    <div>
                        <label className="block text-charcoal font-bold mb-3">
                            How did the meal turn out?
                        </label>
                        <div className="flex justify-center bg-stone-50 p-4 rounded-2xl">
                            {renderStars(outcomeRating, setOutcomeRating)}
                        </div>
                    </div>

                    {/* Helpfulness Rating */}
                    <div>
                        <label className="block text-charcoal font-bold mb-3">
                            How helpful was the app?
                        </label>
                        <p className="text-xs text-stone-400 mb-3">Did the instructions adjust well? Were they clear?</p>
                        <div className="flex justify-center bg-stone-50 p-4 rounded-2xl">
                            {renderStars(helpfulnessRating, setHelpfulnessRating)}
                        </div>
                    </div>

                    {/* Text Feedback */}
                    <div>
                        <label className="block text-charcoal font-bold mb-3">
                            Tell us more <span className="text-stone-400 font-normal text-sm">(Optional)</span>
                        </label>
                        <textarea
                            value={feedback}
                            onChange={(e) => setFeedback(e.target.value)}
                            placeholder="Why did it turn out good or bad? How can we improve?"
                            className="w-full bg-stone-50 border border-stone-200 rounded-2xl p-4 text-stone-700 focus:outline-none focus:ring-2 focus:ring-sage/50 min-h-[120px]"
                        ></textarea>
                    </div>

                    <motion.button
                        whileTap={{ scale: 0.95 }}
                        type="submit"
                        disabled={outcomeRating === 0 || helpfulnessRating === 0}
                        className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${outcomeRating > 0 && helpfulnessRating > 0
                            ? 'bg-terracotta text-stone-900 shadow-lg'
                            : 'bg-stone-200 text-stone-400 cursor-not-allowed'
                            }`}
                    >
                        Submit & Return Home
                    </motion.button>
                </form>
            </motion.div>
        </div>
    );
};

export default RatingView;
