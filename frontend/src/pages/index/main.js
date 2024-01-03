
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
import App from './App.vue'
import RvGrouplist from '@/components/routerViews/RvGrouplist.vue'
import RvGroupview from '@/components/routerViews/RvGroupview.vue'
import RvTasks from '@/components/routerViews/RvTasks.vue'
import RvContacts from '@/components/routerViews/RvContacts.vue'
import RvSettings from '@/components/routerViews/RvSettings.vue'
import RvChats from '@/components/routerViews/RvChats.vue'
import RvCalendar from '@/components/routerViews/RvCalendar.vue'
import RvCall from '@/components/routerViews/RvCall.vue'
import RvFiles from '@/components/routerViews/RvFiles.vue'


/*
	Vue Router
*/
const routes = [
	{ path: '/grouplist', component: RvGrouplist },
	{ path: '/groupview/:group_id', component: RvGroupview },
	{ path: '/tasks', component: RvTasks },
	{ path: '/contacts', component: RvContacts },
	{ path: '/settings', component: RvSettings },
	{ path: '/chats', component: RvChats },
	{ path: '/calendar', component: RvCalendar },
	{ path: '/call', component: RvCall },
	{ path: '/files', component: RvFiles },
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