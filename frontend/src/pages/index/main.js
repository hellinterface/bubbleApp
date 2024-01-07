
/*
	Modules
*/
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Vue3Mq } from "vue3-mq"
import { createRouter, createWebHashHistory } from 'vue-router'
import VueCookies from 'vue-cookies'
import VueClickAway from 'vue3-click-away'
import { useMainStore } from '@/stores/mainStore'
import axios from 'axios';

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
import RvUserview from '@/components/routerViews/RvUserview.vue'

/*
	Vue Router
*/
const routes = [
	{ path: '/grouplist', component: RvGrouplist },
	{ path: '/groupview/:group_id', component: RvGroupview },
	{ path: '/tasks/:board_id', component: RvTasks },
	{ path: '/tasks', component: RvTasks },
	{ path: '/contacts', component: RvContacts },
	{ path: '/settings', component: RvSettings },
	{ path: '/chats/:other_user_id', component: RvChats },
	{ path: '/chats', component: RvChats },
	{ path: '/calendar', component: RvCalendar },
	{ path: '/call', component: RvCall },
	{ path: '/files/:folder_share_link', component: RvFiles },
	{ path: '/files', component: RvFiles },
	{ path: '/user/:user_id', component: RvUserview },
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

var mainStore = useMainStore();

var token = VueCookies.get('access_token');

if (!token) {
	window.location.href = "/login";
}
else {
	mainStore.accessToken = token;
	console.warn("GETTING ME");
	axios.get(location.protocol+"//"+location.hostname+":7070/api/users/me", {withCredentials: true}).then(res => {
		mainStore.currentUser = res.data;
		console.warn("ME", res);
		app.mount('#main');
	})
	.catch(err => {
		console.error("ME", err);
		window.location.href = "/login";
	})
}