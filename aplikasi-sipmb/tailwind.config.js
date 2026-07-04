import defaultTheme from 'tailwindcss/defaultTheme';
import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php',
        './storage/framework/views/*.php',
        './resources/views/**/*.blade.php',
    ],

    theme: {
        extend: {
            fontFamily: {
                sans: ['Figtree', ...defaultTheme.fontFamily.sans],
            },
            colors: {
                brand: {
                    50: '#eef4ff', 100: '#dbe8ff', 200: '#bcd4ff', 300: '#8db6ff',
                    400: '#568eff', 500: '#2d68f7', 600: '#1a49e3', 700: '#1638b8',
                    800: '#152f8f', 900: '#152a6e', 950: '#0f1b45',
                },
                accent: {
                    50: '#fff6ed', 100: '#ffead4', 200: '#ffd1a8', 300: '#ffb070',
                    400: '#ff8737', 500: '#fd6510', 600: '#ee4a06', 700: '#c53608',
                    800: '#9c2c0f', 900: '#7d2710',
                },
            },
        },
    },

    plugins: [forms],
};
