import LoginPage from "./components/LoginPage.vue";
import RegistrationPage from "./components/RegistrationPage.vue";
import DashboardPage from "./components/DashboardPage.vue";
import HomePage from "./components/HomePage.vue";
import DashboardAdmin from "./components/DashboardAdmin.vue";
import ManageCourse from "./components/ManageCourse.vue";
import ManageLectures from "./components/ManageLectures.vue";
import IDE from "./components/IDE.vue";
import CoursePage from "./components/PythonCourse.vue";
import PracticeAssignment from "./components/PracticeAssignment.vue";
import ManageUsers from "./components/ManageUsers.vue";

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
        path: '/dashboard',
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
        name: 'ManageCourse',
        component: ManageCourse,
        // meta: { requiresAuth: true },
        props: true
    },

    {
        path: '/study/lectures',
        name: 'ManageLectures',
        component: ManageLectures,
        // meta: { requiresAuth: true },
        props: true
    },

    {
        path: '/ide',
        name: 'IDE',
        component: IDE,
        // meta: { requiresAuth: true },
        props: true
    },

    {
        path: '/dashboard/4/python',
        name: 'PythonModule',
        component: CoursePage,
        props: true
    },

    {
        path: '/dashboard/pa',
        name: 'PracticeAssignment',
        component: PracticeAssignment,
        props: true
    },

    {
        path: '/user',
        name: 'ManageUsers',
        component: ManageUsers,
        props: true
    },

]
const router = createRouter({
    history: createWebHistory(),
    routes
})
export default router