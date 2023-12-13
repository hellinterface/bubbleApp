<template>
	<div class="headerButtonSet">
		<XButton icon_name="add" appearance="outlined">Добавить контакт</XButton>
	</div>
</template>

<script>
//import { ref } from 'vue
import XButton from '@/components/elements/XButton.vue';

export default {
	name: 'hbsContacts',
	components: {
		XButton
	},
	mounted() {
	}
}
</script>

<style scoped>
</style>
