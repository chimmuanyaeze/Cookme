import React from 'react';
import { motion } from 'framer-motion';

const FloatingBubble = ({ label, icon, color = 'bg-white text-black', onClick }) => {
    return (
        <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onClick}
            className={`flex flex-col items-center justify-center w-24 h-24 rounded-full shadow-[0_4px_20px_rgba(0,0,0,0.05)] ${color} border border-white/20 backdrop-blur-sm transition-shadow hover:shadow-[0_8px_30px_rgba(0,0,0,0.1)]`}
        >
            <span className="text-3xl mb-1">{icon}</span>
            <span className="text-xs font-medium tracking-wide">{label}</span>
        </motion.button>
    );
};

export default FloatingBubble;
