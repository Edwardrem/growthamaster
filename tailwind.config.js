/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/views.py',
    './**/forms.py',
  ],
  theme: {
    extend: {
      colors: {
        'brand-navy':     '#10222E',
        'brand-red':      '#F35236',
        'brand-darkred':  '#B13921',
        'brand-cream':    '#FFF3D9',
        'brand-offwhite': '#FDF8F4',
        'brand-muted':    '#B9C9C9',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
        display: ['Oswald', 'Inter', 'ui-sans-serif', 'system-ui'],
      },
    },
  },
  plugins: [],
}
