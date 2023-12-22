<template>
	<div class="headerButtonSet">
		<XButton icon_name="call_end" appearance="outlined">Выйти из собрания</XButton>
	</div>
</template>

<script>
//import { ref } from 'vue
import XButton from '@/components/elements/XButton.vue';

export default {
	name: 'HbsCall',
	components: {
		XButton
	},
	mounted() {
	}
}
</script>

<style scoped>
</style>
