
/*
	Modules
*/
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Vue3Mq } from "vue3-mq";
import { createRouter, createWebHashHistory } from 'vue-router'
import VueCookies from 'vue-cookies'

/*
	CSS
*/
import '../assets/css/standard.css';

/*
	Components
*/
import App from './App.vue'
import RvGrouplist from '../components/routerViews/RvGrouplist.vue'
import RvGroupview from '../components/routerViews/RvGroupview.vue'
import RvTasks from '../components/routerViews/RvTasks.vue'
import RvContacts from '../components/routerViews/RvContacts.vue'
import RvSettings from '../components/routerViews/RvSettings.vue'
import RvChats from '../components/routerViews/RvChats.vue'
import RvCalendar from '../components/routerViews/RvCalendar.vue'


/*
	Vue Router
*/
const routes = [
	{ path: '/grouplist', component: RvGrouplist },
	{ path: '/groupview', component: RvGroupview },
	{ path: '/tasks', component: RvTasks },
	{ path: '/contacts', component: RvContacts },
	{ path: '/settings', component: RvSettings },
	{ path: '/chats', component: RvChats },
	{ path: '/calendar', component: RvCalendar },
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
const app = createApp(App);
app.use(router);
app.use(pinia);
app.use(VueCookies);
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