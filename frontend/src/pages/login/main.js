import { createApp } from 'vue'
import VueCookies from 'vue-cookies'
import LoginPage from './LoginPage.vue'
import '@/assets/css/standard.css';
import '@/assets/css/login_signup.css';

const app = createApp(LoginPage);
app.use(VueCookies);
app.mount('#main');
