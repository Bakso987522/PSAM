import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/styles/main.css'],
  runtimeConfig: {
    apiUrl: '',
  },
  vite: {
    plugins: [tailwindcss()]
  }
})
