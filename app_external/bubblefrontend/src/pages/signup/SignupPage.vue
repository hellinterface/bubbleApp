<template>
	<div id="mainContainer">
		<img src="@/assets/images/logo_small_mono_2.svg" alt="Bubble" id="headerLogo">
		<header>
			<img src="@/assets/images/logo_text.svg" alt="Bubble" id="headerTextLogo">
			<div>| Регистрация</div>
		</header>
		<div id="formContainer">
			<LabeledInput name="email" type="text" placeholder="">Почта</LabeledInput>
			<LabeledInput name="handle" type="text" placeholder="">Имя пользователя</LabeledInput>
			<LabeledInput name="visible_name" type="text" placeholder="">Публичное имя</LabeledInput>
			<LabeledInput name="password" type="password" placeholder="">Пароль</LabeledInput>
			<button>Создать аккаунт</button>
			<a href="/login">Войти в существующий аккаунт</a>
		</div>
	</div>
</template>

<script>
	import LabeledInput from "@/components/LabeledInput.vue";

	export default {
		name: 'SignupPage',
		components: {
			LabeledInput
		}
	}
</script>

<style>
</style>