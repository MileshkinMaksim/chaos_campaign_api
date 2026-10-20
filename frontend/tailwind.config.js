/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bt: {
          bg: '#0F172A',         // Slate 900
          card: '#1E293B',       // Slate 800
          border: '#334155',     // Slate 700
          amber: '#F59E0B',      // Акцент Warchest / SP
          green: '#10B981',      // Акцент успеха / Операбелен
          red: '#EF4444',        // Критические повреждения / Уничтожен
          blue: '#3B82F6',       // Опыт XP / Пилоты
        }
      }
    },
  },
  plugins: [],
}