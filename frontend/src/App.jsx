import React, { useState, useEffect } from 'react';
import SplashWhisk from './components/SplashWhisk';
import HomeView from './views/HomeView';
import SearchView from './views/SearchView';
import CookedView from './views/CookedView';
import SavedView from './views/SavedView';
import ProfileView from './views/ProfileView';
import RecipeDetailView from './views/RecipeDetailView';
import TransitionSplash from './views/TransitionSplash';
import ModeSelectView from './views/ModeSelectView';
import CookingView from './views/CookingView';
import RatingView from './views/RatingView';
import BottomNav from './components/BottomNav';
import { AnimatePresence } from 'framer-motion';

function App() {
    const [showSplash, setShowSplash] = useState(true);
    const [currentView, setCurrentView] = useState('home');
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [cookingConfig, setCookingConfig] = useState({ mode: 'manual', voice: 'female', missingIngredients: [] });

    const handleRecipeSelect = (recipe) => {
        setSelectedRecipe(recipe);
        setCurrentView('detail');
    };

    const handlePrepareCooking = (nextView, data = {}) => {
        if (data.missingOptional) {
            setCookingConfig(prev => ({ ...prev, missingIngredients: data.missingOptional }));
        }
        setCurrentView(nextView); // Normally 'transition_splash'
    };

    const handleModeSelectStart = (config) => {
        setCookingConfig(prev => ({ ...prev, ...config }));
        setCurrentView('cooking');
    };

    const showBottomNav = ['home', 'search', 'cooked', 'saved', 'profile'].includes(currentView);

    return (
        <>
            <AnimatePresence>
                {showSplash && (
                    <SplashWhisk onComplete={() => setShowSplash(false)} />
                )}
            </AnimatePresence>

            {!showSplash && (
                <div className="min-h-screen bg-beige relative overflow-x-hidden">
                    <div className="flour-texture"></div>

                    <main className={showBottomNav ? "pb-24" : ""}>
                        {currentView === 'home' && <HomeView onSelectRecipe={handleRecipeSelect} />}
                        {currentView === 'search' && <SearchView />}
                        {currentView === 'cooked' && <CookedView onStartCooking={() => setCurrentView('home')} />}
                        {currentView === 'saved' && <SavedView />}
                        {currentView === 'profile' && <ProfileView />}

                        <AnimatePresence>
                            {currentView === 'detail' && selectedRecipe && (
                                <RecipeDetailView
                                    recipe={selectedRecipe}
                                    onBack={() => setCurrentView('home')}
                                    onStartCooking={(view, data) => handlePrepareCooking(view, data)}
                                />
                            )}
                        </AnimatePresence>

                        <AnimatePresence>
                            {currentView === 'transition_splash' && (
                                <TransitionSplash onComplete={() => setCurrentView('mode_select')} />
                            )}
                        </AnimatePresence>

                        <AnimatePresence>
                            {currentView === 'mode_select' && (
                                <ModeSelectView
                                    onBack={() => setCurrentView('detail')}
                                    onStart={handleModeSelectStart}
                                />
                            )}
                        </AnimatePresence>

                        <AnimatePresence>
                            {currentView === 'cooking' && selectedRecipe && (
                                <CookingView
                                    recipe={selectedRecipe}
                                    mode={cookingConfig.mode}
                                    voiceGender={cookingConfig.voice} // We can pass voice gender down too
                                    missingIngredients={cookingConfig.missingIngredients} // Pass missing to adapt steps
                                    onExit={() => setCurrentView('detail')}
                                    onFinish={() => setCurrentView('rating')} // Placeholder for rating view
                                />
                            )}
                        </AnimatePresence>
                        <AnimatePresence>
                            {currentView === 'rating' && (
                                <RatingView onComplete={() => setCurrentView('home')} />
                            )}
                        </AnimatePresence>
                    </main>

                    {showBottomNav && (
                        <BottomNav currentView={currentView} onViewChange={setCurrentView} />
                    )}
                </div>
            )}
        </>
    );
}

export default App;
