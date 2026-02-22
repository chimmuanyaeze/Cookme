import React, { useEffect } from 'react';
import { motion } from 'framer-motion';

const SplashWhisk = ({ onComplete }) => {
    useEffect(() => {
        const timer = setTimeout(onComplete, 2500);
        return () => clearTimeout(timer);
    }, [onComplete]);

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-beige">
            <motion.div
                initial={{ opacity: 0, y: 100 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{
                    type: "spring",
                    stiffness: 120,
                    damping: 20,
                    duration: 1.5
                }}
                className="flex flex-col items-center"
            >
                {/* Minimalist Whisk SVG */}
                <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#2F2F2F" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M7 16l-3 6" />
                    <path d="M17 16l3 6" />
                    <path d="M12 2v10" />
                    <path d="M12 12c-3.5 0-6 2.5-6 6 0 1.5 0.5 2.5 1 3" />
                    <path d="M12 12c3.5 0 6 2.5 6 6 0 1.5-0.5 2.5-1 3" />
                    <path d="M12 21a5 5 0 0 1-5-5c0-1.5.5-2.5 1-3" />
                    <path d="M12 21a5 5 0 0 0 5-5c0-1.5-.5-2.5-1-3" />
                </svg>

                <motion.h1
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5, duration: 1 }}
                    className="mt-4 text-2xl font-serif text-charcoal tracking-widest uppercase"
                >
                    Culinara
                </motion.h1>
            </motion.div>
        </div>
    );
};

export default SplashWhisk;
