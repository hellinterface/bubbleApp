
/*
	Modules
*/
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Vue3Mq } from "vue3-mq"
import { createRouter, createWebHashHistory } from 'vue-router'
import VueCookies from 'vue-cookies'
import VueClickAway from 'vue3-click-away'

/*
	CSS
*/
import '@/assets/css/standard.css'
import '@/assets/fonts/helvetica.css'

/*
	Components
*/
import AdminPanel from './AdminPanel.vue'
import ArvUsers from '@/components/admin/ArvUsers.vue'


/*
	Vue Router
*/
const routes = [
	{ path: '/users', component: ArvUsers },
];

const router = createRouter({
	history: createWebHashHistory(),
	routes: routes,
});

/*
	Pinia
*/
const pinia = createPinia();

/*
	App
*/
const app = createApp(AdminPanel);
app.use(router);
app.use(pinia);
app.use(VueCookies);
app.use(VueClickAway);
// Breakpoints taken from default 'bootstrap5' preset (https://vue3-mq.info/configure/presets.html)
app.use(Vue3Mq, {
	breakpoints: {
		xs: 0,
		sm: 576,
		md: 768,
		lg: 992,
		xl: 1200,
		xxl: 1400
	}
});
app.mount('#main');