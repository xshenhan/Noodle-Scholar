// router.js
// import Vue from 'vue';
// import Router from 'vue-router';
// import Paper from './components/paper.vue';

// Vue.use(Router);

// export default new Router({
//   routes: [
//     {
//       path: '/paper/:id',
//       name: 'paper',
//       component: Paper
//     }
//   ]
// });
import { createRouter, createWebHistory } from 'vue-router';
import Paper from './components/paper.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/paper/:id',
      name: 'paper',
      component: Paper
    }
  ]
});

export default router;
