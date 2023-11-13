<template>
	<div id="mainContainer">
		<img src="@/assets/images/logo_small_mono_2.svg" alt="Bubble" id="headerLogo">
		<header>
			<img src="@/assets/images/logo_text.svg" alt="Bubble" id="headerTextLogo">
			<div>| Вход</div>
		</header>
		<div id="formContainer">
			<LabeledInput name="email" type="text" placeholder="" ref="input_email" v-model="value_email">Почта</LabeledInput>
			<LabeledInput name="password" type="password" placeholder="" ref="input_password" v-model="value_password">Пароль</LabeledInput>
			<XButton @onclick="makeQuery()">Войти</XButton>
			<a href="/signup">Создать аккаунт</a>
		</div>
	</div>
</template>

<script>
	import { inject, ref } from 'vue'
	import axios from 'axios';
	import LabeledInput from "@/components/LabeledInput.vue";
	import XButton from "@/components/elements/XButton.vue";

	export default {
		name: 'LoginPage',
		components: {
			LabeledInput,
			XButton
		},
		setup() {
			const $cookies = inject('$cookies');
			const input_email = ref(null);
			const input_password = ref(null);
			const value_email = ref(null);
			const value_password = ref(null);
			async function sha256(message) {
				const msgBuffer = new TextEncoder().encode(message);
				const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
				const hashArray = Array.from(new Uint8Array(hashBuffer));
				const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
				return hashHex;
			}
			function makeQuery() {
				console.log(value_email.value);
				console.log(value_password.value);
				sha256(value_password.value).then(password_hash => {
					axios.post('http://localhost:7070/api/auth/login', {email: value_email.value, password_hash: password_hash})
					.then(function (response) {
						console.log(response.data);
						$cookies.set('access_token', response.data.access_token)
						setTimeout(() => window.location.href = "/", 1000);
					})
					.catch(function (error) {
						console.log(error);
					});
				});
			}
			return {
				makeQuery,
				input_email,
				input_password,
				value_email,
				value_password
			}
		},
	}
</script>

<style>
</style>