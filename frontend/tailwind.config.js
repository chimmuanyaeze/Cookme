/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                beige: {
                    DEFAULT: '#F5F5DC', // Warm Beige / Linen
                    dark: '#E8E8C8',
                },
                charcoal: '#2F2F2F', // Primary Text / Cast Iron
                sage: '#8A9A5B', // Success / Fresh Herbs
                terracotta: '#E2725B', // Highlight / Clay
                ceramic: '#FFFFFF', // Card Bg
            },
            borderRadius: {
                'xl': '24px', // Ceramic feel
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'], // Clean modern feel
                serif: ['Merriweather', 'serif'], // Rustic feel
            },
            backgroundImage: {
                'wood-pattern': "url('https://www.transparenttextures.com/patterns/wood-pattern.png')",
            }
        },
    },
    plugins: [],
}
