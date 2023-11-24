import { createApp } from 'vue'
import Vue from 'vue'
import dev from './App.vue'
import axios from 'axios'
// Vue.prototype.$http = axios
import router from './router';

// createApp(dev).mount('#app')
new Vue({
    router,
    render: h => h(dev)
  }).$mount('#app');
