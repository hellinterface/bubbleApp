<template>
	<div id="mainContainer">
		<img src="@/assets/images/logo_small_mono_2.svg" alt="Bubble" id="headerLogo">
		<header>
			<img src="@/assets/images/logo_text.svg" alt="Bubble" id="headerTextLogo">
		</header>
		<div class="errorMessage" v-if="isErrored"><icon>warning</icon>Возникла ошибка.</div>
		<div id="formContainer">
			<LabeledInput name="email" type="text" placeholder="" v-model="value_email">Почта</LabeledInput>
			<LabeledInput name="handle" type="text" placeholder="" v-model="value_handle">Имя пользователя</LabeledInput>
			<LabeledInput name="visible_name" type="text" placeholder="" v-model="value_visible_name">Публичное имя</LabeledInput>
			<LabeledInput name="password" type="password" placeholder="" v-model="value_password">Пароль</LabeledInput>
			<XButton @onclick="makeQuery()">Создать аккаунт</XButton>
			<a href="/login">Войти в существующий аккаунт</a>
		</div>
	</div>
</template>

<script>
import { inject, ref } from 'vue'
import axios from 'axios';
import LabeledInput from "@/components/LabeledInput.vue";
import XButton from "@/components/elements/XButton.vue";

const isErrored = ref(false);

export default {
	name: 'LoginPage',
	components: {
		LabeledInput,
		XButton
	},
	setup() {
		const $cookies = inject('$cookies');
		const value_email = ref(null);
		const value_handle = ref(null);
		const value_visible_name = ref(null);
		const value_password = ref(null);
		async function sha256(message) {
			const msgBuffer = new TextEncoder().encode(message);
			const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
			const hashArray = Array.from(new Uint8Array(hashBuffer));
			const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
			return hashHex;
		}
		function makeQuery() {
			sha256(value_password.value).then(password_hash => {
				let requestObject = {email: value_email.value, handle: value_handle.value, visible_name: value_visible_name.value, password_hash: password_hash};
				axios.post(location.protocol+'//localhost:7070/api/auth/signup', requestObject)
				.then(function (response) {
					console.log(response.data);
					$cookies.set('access_token', response.data.access_token)
					setTimeout(() => window.location.href = "/app", 500);
				})
				.catch(function (error) {
					console.log(error);
						isErrored.value = true;
				});
			});
		}
		return {
			makeQuery,
			value_email,
			value_handle,
			value_visible_name,
			value_password,
			isErrored
		}
	}
}
</script>

<style>
</style>