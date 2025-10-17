import type { Config } from 'tailwindcss'

export default {
  content: [
    './index.html',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          DEFAULT: '#7c3aed',
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
        },
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        petal: {
          primary: '#FFB3B3', // Peach Pink
          secondary: '#D2B4DE', // Lavender
          accent: '#AFFEEB', // Mint
          neutral: '#5D5463', // Soft ink for text
          'base-100': '#FEFBF6', // Ivory white background
          info: '#D2B4DE',
          success: '#AFFEEB',
          warning: '#FFF5B7',
          error: '#F5A3A3',
        },
      },
    ],
  },
} satisfies Config


