import React, { useEffect } from 'react';
import { motion } from 'framer-motion';

const TransitionSplash = ({ onComplete }) => {
    useEffect(() => {
        // Mock loading time
        const timer = setTimeout(() => {
            onComplete();
        }, 2000);
        return () => clearTimeout(timer);
    }, [onComplete]);

    return (
        <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-terracotta text-white">
            <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 1.2, opacity: 0 }}
                transition={{ duration: 0.5, ease: "easeOut" }}
                className="flex flex-col items-center"
            >
                {/* Spatula Loader Animation */}
                <motion.div
                    animate={{ rotate: [-20, 20, -20] }}
                    transition={{ repeat: Infinity, duration: 1, ease: "easeInOut" }}
                    className="text-6xl mb-6 shadow-xl"
                >
                    🍳
                </motion.div>

                <h1 className="text-3xl font-serif text-center mb-2 italic px-6 leading-tight">
                    Getting ready to cook, chef...
                </h1>

                <div className="mt-8 flex gap-2">
                    {[0, 1, 2].map((i) => (
                        <motion.div
                            key={i}
                            animate={{ y: [0, -10, 0] }}
                            transition={{ repeat: Infinity, duration: 0.6, delay: i * 0.1 }}
                            className="w-2 h-2 rounded-full bg-white/50"
                        />
                    ))}
                </div>
            </motion.div>
        </div>
    );
};

export default TransitionSplash;
