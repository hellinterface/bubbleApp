
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


/*
	Vue Router
*/
const routes = [
	{ path: '/app/grouplist', component: RvGrouplist },
	{ path: '/app/groupview/:group_id', component: RvGroupview },
	{ path: '/app/tasks', component: RvTasks },
	{ path: '/app/contacts', component: RvContacts },
	{ path: '/app/settings', component: RvSettings },
	{ path: '/app/chats', component: RvChats },
	{ path: '/app/calendar', component: RvCalendar },
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