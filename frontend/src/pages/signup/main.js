import { createApp } from 'vue'
import VueCookies from 'vue-cookies'
import SignupPage from './SignupPage.vue'
import '@/assets/css/standard.css';
import '@/assets/css/login_signup.css';
import '@/assets/fonts/helvetica.css'

const app = createApp(SignupPage);
app.use(VueCookies);
app.mount('#main');
