import {createRouter, createWebHashHistory} from 'vue-router'
import Hands_on from "@/components/Hands_on.vue";
import Know_more from "@/components/Know_more.vue";
import Test_yourself from "@/components/Test_yourself.vue";

const routes = [
    {
        path: '/',
        name: 'home',
        redirect: "Know_more"
    },
    { name: "Hands_on", path: "/Hands_on", component: Hands_on },
    { name: "Test_yourself", path: "/Test_yourself", component: Test_yourself },
    { name: "Know_more", path: "/Know_more", component: Know_more },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
});

export default router
