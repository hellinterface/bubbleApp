<template>
	<div class="headerButtonSet">
		<XButton icon_name="add" appearance="outlined" @click="createColumn()">Создать столбец</XButton>
	</div>
</template>

<script>
//import { ref } from 'vue
import XButton from '@/components/elements/XButton.vue';
//import { useMainStore } from '@/stores/mainStore';

//var mainStore;

export default {
	name: 'HbsTasks',
	components: {
		XButton
	},
	methods: {
		createColumn() {
			console.warn("SHOULD CREATE COLUMN HERE");
		}
	},
	setup() {
		//mainStore = useMainStore();
	},
	mounted() {
	}
}
</script>

<style scoped>
</style>
