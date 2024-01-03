
/*
	CSS
*/
import { createApp } from 'vue'
import LandingMain from './LandingMain.vue'
import '@/assets/css/landing.css'
import '@/assets/fonts/helvetica.css'
import '@/assets/fonts/russoone.css'

const app = createApp(LandingMain);
app.mount('#main');