import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Searchresult from '../components/Searchresult.vue'

const history = createWebHistory();
const router = createRouter({
    history: history,
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home
        },
        {
            path: '/searchresult',
            name: 'Searchresult',
            component: Searchresult
        }
    ]
});

// const router = createRouter({
//     history: createWebHistory(process.env.BASE_URL),
//     routes
// })

export default router