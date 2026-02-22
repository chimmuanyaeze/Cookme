import React from 'react';

const DisplayScreen = ({ content, subContent, status }) => {
    return (
        <div className="relative w-full bg-gray-800 rounded-lg border-b-2 border-r-2 border-white/10 shadow-[inset_0_4px_8px_rgba(0,0,0,0.8)] p-4 overflow-hidden mb-6">
            {/* Scanlines effect */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] z-10 pointer-events-none bg-[length:100%_4px,3px_100%]"></div>

            {/* Glowing Text */}
            <div className="relative z-20 font-mono text-green-400 text-shadow-[0_0_5px_rgba(74,222,128,0.6)]">
                <div className="flex justify-between items-center border-b border-green-800/50 pb-2 mb-2">
                    <span className="text-xs uppercase tracking-widest opacity-70">AI Chef OS v2.0</span>
                    <span className="text-xs animate-pulse">{status || "READY"}</span>
                </div>

                <div className="min-h-[120px] flex flex-col justify-center">
                    <h2 className="text-xl md:text-2xl font-bold mb-2 leading-tight">{content}</h2>
                    {subContent && <p className="text-sm md:text-base opacity-80">{subContent}</p>}
                </div>
            </div>

            {/* Screen reflection/glare */}
            <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-white/5 to-transparent skew-x-12 pointer-events-none"></div>
        </div>
    );
};

export default DisplayScreen;
