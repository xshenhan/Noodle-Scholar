import { createApp } from 'vue'
import dev from './App.vue' // 开发分支
import axios from 'axios'
import hw from './homework.vue' // 作业分支
Vue.prototype.$http = axios

createApp(dev).mount('#app')
createApp(hw).mount('#hw')
