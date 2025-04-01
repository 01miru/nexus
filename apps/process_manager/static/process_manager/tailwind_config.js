tailwind.config = {
    theme: {
        extend: {
            colors: {
                'dark': {
                    50: '#1a1a2e',
                    100: '#16213e',
                    200: '#0f3460',
                    300: '#3d5af1'
                }
            },
            animation: {
                'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            }
        }
    }
}