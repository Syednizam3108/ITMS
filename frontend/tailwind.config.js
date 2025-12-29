export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      animation: {
        'blob': 'blob 7s infinite',
      },
      keyframes: {
        blob: {
          '0%, 100%': { 
            transform: 'translate(0, 0) scale(1)',
          },
          '33%': { 
            transform: 'translate(30px, -50px) scale(1.1)',
          },
          '66%': { 
            transform: 'translate(-20px, 20px) scale(0.9)',
          },
        }
      }
    },
  },
  plugins: [],
  safelist: [
    'text-blue-400',
    'text-green-400',
    'text-purple-400',
    'text-orange-400',
    'bg-blue-500/20',
    'bg-green-500/20',
    'bg-red-500/20',
    'border-blue-500/30',
    'border-green-500/30',
    'border-red-500/30',
  ]
}
