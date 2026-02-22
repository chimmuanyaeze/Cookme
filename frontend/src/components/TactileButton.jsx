import React from 'react';

const TactileButton = ({ onClick, label, color = "gray", size = "md", active = false }) => {
    // Skeuomorphic styles
    const baseStyle = "relative flex items-center justify-center rounded-full transition-all active:scale-95 focus:outline-none select-none";

    const sizeClasses = {
        sm: "w-12 h-12 text-xs",
        md: "w-20 h-20 text-sm font-bold",
        lg: "w-28 h-28 text-lg font-bold",
        xl: "w-32 h-32 text-xl font-bold"
    };

    // Gradients and Shadows for 3D effect
    const colorClasses = {
        gray: "bg-gradient-to-b from-gray-200 to-gray-400 border-4 border-gray-300 shadow-[inset_0_1px_0_rgba(255,255,255,0.4),0_4px_6px_rgba(0,0,0,0.4)] active:shadow-[inset_0_2px_4px_rgba(0,0,0,0.4)] active:translate-y-1",
        red: "bg-gradient-to-b from-red-400 to-red-600 border-4 border-red-300 shadow-[inset_0_1px_0_rgba(255,255,255,0.4),0_4px_6px_rgba(0,0,0,0.4)] text-white active:shadow-[inset_0_2px_4px_rgba(0,0,0,0.6)] active:translate-y-1",
        green: "bg-gradient-to-b from-green-400 to-green-600 border-4 border-green-300 shadow-[inset_0_1px_0_rgba(255,255,255,0.4),0_4px_6px_rgba(0,0,0,0.4)] text-white active:shadow-[inset_0_2px_4px_rgba(0,0,0,0.6)] active:translate-y-1",
        blue: "bg-gradient-to-b from-blue-400 to-blue-600 border-4 border-blue-300 shadow-[inset_0_1px_0_rgba(255,255,255,0.4),0_4px_6px_rgba(0,0,0,0.4)] text-white active:shadow-[inset_0_2px_4px_rgba(0,0,0,0.6)] active:translate-y-1",
    };

    // Indicator light (optional)
    const indicatorClass = active
        ? "absolute top-2 right-2 w-2 h-2 rounded-full bg-green-400 shadow-[0_0_8px_2px_rgba(74,222,128,0.8)]"
        : "hidden";

    return (
        <button
            onClick={onClick}
            className={`${baseStyle} ${sizeClasses[size]} ${colorClasses[color]} group`}
        >
            <div className={indicatorClass}></div>
            <span className="drop-shadow-sm z-10">{label}</span>
            {/* Texture overlay (noise) - simplified as opacity layer */}
            <div className="absolute inset-0 rounded-full bg-white opacity-10 pointer-events-none mix-blend-overlay"></div>
        </button>
    );
};

export default TactileButton;
