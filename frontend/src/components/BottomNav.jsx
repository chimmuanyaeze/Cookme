import React from 'react';

const BottomNav = ({ currentView, onViewChange }) => {
    const navItems = [
        { id: 'home', label: 'Home', icon: '🏠' },
        { id: 'search', label: 'Search', icon: '🍳' }, // Frying pan for search as requested
        { id: 'cooked', label: 'Cooked', icon: '👨‍🍳' }, // Chef hat for cooked
        { id: 'saved', label: 'Saved', icon: '🧊' }, // Fridge for saved
        { id: 'profile', label: 'Profile', icon: '👤' },
    ];

    return (
        <div className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-stone-100 border-t border-stone-200 px-6 py-2 pb-6 z-40 flex justify-between items-center rounded-t-3xl shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
            {navItems.map((item) => (
                <button
                    key={item.id}
                    onClick={() => onViewChange(item.id)}
                    className={`flex flex-col items-center justify-center p-2 transition-all duration-200 ${currentView === item.id
                            ? 'text-terracotta transform -translate-y-1'
                            : 'text-stone-400 hover:text-stone-600'
                        }`}
                >
                    <span className="text-2xl mb-1">{item.icon}</span>
                    <span className="text-[10px] font-medium tracking-wide">{item.label}</span>
                </button>
            ))}
        </div>
    );
};

export default BottomNav;
