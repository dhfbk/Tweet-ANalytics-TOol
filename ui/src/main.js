import {createApp} from 'vue'
import App from './App.vue'

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle";
import "bootstrap-icons/font/bootstrap-icons.css"
import "./style.css";
import router from './router'

import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

createApp(App)
    .use(router)
    .component('VueDatePicker', VueDatePicker)
    .mount('#app')

