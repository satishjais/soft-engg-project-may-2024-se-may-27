import LoginPage from "./components/LoginPage.vue";
import RegistrationPage from "./components/RegistrationPage.vue";
// import DashboardPage from "./components/DashboardPage.vue";
import {
    createRouter,createWebHistory
}
from "vue-router"

const routes=[
    {
        name:'LoginPage',
        component:LoginPage,
        path:'/login'
    },
    {
        name:'RegistrationPage',
        component:RegistrationPage,
        path:'/register'
    },
    // {
    //     name:'DashboardPage',
    //     component:DashboardPage,
    //     path:'/dashboard'
    // },
    
]
const router=createRouter({
    history:createWebHistory(),
    routes
})
export default router