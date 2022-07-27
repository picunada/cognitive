import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/css/bootstrap-reboot.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import VueGoodTablePlugin from 'vue-good-table-next';
// import Vue from 'vue'

// import the styles 
import 'vue-good-table-next/dist/vue-good-table-next.css'
import './css_theme/dist/css/theme.css'

// Vue.use(VueGoodTablePlugin);


import 'bootstrap/dist/js/bootstrap.js'
import '@fortawesome/fontawesome-free/js/all'
import components from "@/components";
import store from "@/store";

const app = createApp(App)

components.forEach(component => {
    app.component(component.name, component)
})

app.use(router).use(store)
app.mount('#app')

