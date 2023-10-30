<template>
	<div id="mainContainer">
		<img src="@/assets/images/logo_small_mono_2.svg" alt="Bubble" id="headerLogo">
		<header>
			<img src="@/assets/images/logo_text.svg" alt="Bubble" id="headerTextLogo">
			<div>| Вход</div>
		</header>
		<div id="formContainer">
			<LabeledInput name="email" type="text" placeholder="">Почта</LabeledInput>
			<LabeledInput name="password" type="password" placeholder="">Пароль</LabeledInput>
			<button>Войти</button>
			<a href="/signup">Создать аккаунт</a>
		</div>
	</div>
</template>

<script>
	import LabeledInput from "../components/LabeledInput.vue";

	export default {
		name: 'LoginPage',
		components: {
			LabeledInput
		}
	}
</script>

<style>
</style>