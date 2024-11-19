// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: ['@nuxt/ui', '@pinia/nuxt'],
  colorMode: {
    preference: 'dark',
  },
  app: {
    head: {
      script: [{
        src: "//cdn.socket.io/socket.io-1.1.0.js"
      },{
        src: "//beebotte.com/bbt.js"
      }]
    }
  }
})