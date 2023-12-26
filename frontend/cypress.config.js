// const { defineConfig } = require('cypress')

// module.exports = defineConfig({
//   e2e: {
//     specPattern: 'cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}',
//     baseUrl: 'http://localhost:4173'
//   },
//   component: {
//     specPattern: 'src/**/__tests__/*.{cy,spec}.{js,ts,jsx,tsx}',
//     devServer: {
//       framework: 'vue',
//       bundler: 'vite'
//     }
//   }
// })
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  assersDir: 'static'
})
