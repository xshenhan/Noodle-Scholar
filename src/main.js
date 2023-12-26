import { createApp } from 'vue'
import dev from './App.vue'
import router from './router/'
// import * as marked from 'marked';

// createApp(dev).mount('#app')
createApp(dev).use(router).mount('#app')
