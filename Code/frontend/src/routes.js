import LoginPage from "./components/LoginPage.vue";
import RegistrationPage from "./components/RegistrationPage.vue";
import DashboardPage from "./components/DashboardPage.vue";
import HomePage from "./components/HomePage.vue";
import DashboardAdmin from "./components/DashboardAdmin.vue";
import ManageCourses from "./components/ManageCourses.vue";
import {
    createRouter,
    createWebHistory
}
from "vue-router"

const routes = [{
        name: 'LoginPage',
        component: LoginPage,
        path: '/login'
    },
    {
        name: 'RegistrationPage',
        component: RegistrationPage,
        path: '/register'
    },
    {
        name: 'HomePage',
        component: HomePage,
        path: '/'
    },
    {
        path: '/dashboard/:userId',
        name: 'DashboardBoard',
        component: DashboardPage,
        // meta: { requiresAuth: true },
        props: true
    },
    {
        path: '/dashboard/admin',
        name: 'DashboardAdmin',
        component: DashboardAdmin,
        // meta: { requiresAuth: true },
        props: true
    },

    {
        path: '/study',
        name: 'ManageCourses',
        component: ManageCourses,
        // meta: { requiresAuth: true },
        props: true
    },

]
const router = createRouter({
    history: createWebHistory(),
    routes
})
export default router