import React from 'react';
import { motion } from 'framer-motion';

const StepCard = ({ step, onComplete, onBack, isLast }) => {
    if (!step) return null;

    return (
        <div className="h-full bg-white rounded-t-[3rem] shadow-[0_-10px_40px_rgba(0,0,0,0.05)] mt-6 p-8 flex flex-col items-center justify-center text-center">
            <h2 className="text-stone-400 font-medium uppercase tracking-widest text-sm mb-6">
                Step {step.step_number || 1}
            </h2>

            <p className="text-2xl font-serif text-charcoal leading-relaxed mb-12 max-w-sm">
                {step.instruction || 'No instruction available for this step.'}
            </p>

            {step.timer && (
                <div className="mb-12">
                    <div className="w-32 h-32 rounded-full border-4 border-sage flex items-center justify-center text-2xl font-serif text-charcoal">
                        {step.timer}m
                    </div>
                </div>
            )}

            <div className="flex gap-4 mt-auto">
                <button
                    onClick={onBack}
                    className="px-6 py-4 rounded-full border border-stone-200 text-stone-500 font-medium hover:bg-stone-50 transition-colors"
                >
                    Back
                </button>
                <button
                    onClick={onComplete}
                    className="px-8 py-4 rounded-full bg-terracotta text-stone-900 font-bold shadow-md hover:shadow-lg transition-shadow"
                >
                    {isLast ? 'Finish Recipe' : 'Next Step'}
                </button>
            </div>
        </div>
    );
};

export default StepCard;
