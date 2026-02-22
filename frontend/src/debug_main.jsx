import React from 'react';
import { createRoot } from 'react-dom/client';

console.log("Debug Main Mounted");

function DebugApp() {
    return (
        <div style={{ backgroundColor: 'red', color: 'white', padding: '20px', height: '100vh' }}>
            <h1>DEBUG MODE</h1>
            <p>If you see this, React is working.</p>
        </div>
    );
}

try {
    const root = createRoot(document.getElementById('root'));
    root.render(<DebugApp />);
    console.log("Debug Render called");
} catch (e) {
    console.error("Debug Render Failed", e);
    document.body.innerHTML = "<h1>CRITICAL ERROR: " + e.message + "</h1>";
}
