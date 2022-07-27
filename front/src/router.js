import { createRouter, createWebHashHistory } from "vue-router";
import ClientList from '@/components/ClientList.vue'


export default createRouter({
    history: createWebHashHistory(),
    routes: [
        {path: '/client-list', component: ClientList}
    ]
})