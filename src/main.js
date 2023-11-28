import { createApp } from 'vue'
import dev from './App.vue'
import router from './router/'

// createApp(dev).mount('#app')
createApp(dev).use(router).mount('#app')
