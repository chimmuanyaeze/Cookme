export const antigravity = {
    // "Low Gravity / High Friction"
    hover: {
        y: -5,
        transition: {
            type: "spring",
            stiffness: 300,
            damping: 15, // High friction to stop wobble
            mass: 0.8,   // Light feel
        }
    },
    tap: {
        scale: 0.98,
        transition: {
            type: "spring",
            stiffness: 400,
            damping: 10
        }
    },
    float: {
        y: [0, -8, 0],
        transition: {
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut"
        }
    },
    entrance: {
        hidden: { opacity: 0, y: 50 },
        visible: (custom) => ({
            opacity: 1,
            y: 0,
            transition: {
                delay: custom * 0.1,
                type: "spring",
                stiffness: 100,
                damping: 20
            }
        })
    }
};
