import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/styles/main.css'],
  modules: ['reka-ui/nuxt'],
  runtimeConfig: {
    apiUrl: '',
  },
  vite: {
    plugins: [tailwindcss()]
  }
})
