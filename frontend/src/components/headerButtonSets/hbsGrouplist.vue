<template>
	<div class="headerButtonSet">
		<XButton icon_name="add" appearance="outlined" @click="showDialog_groupCreate()">Создать группу</XButton>
	</div>
</template>

<script>
//import { ref } from 'vue
import XButton from '@/components/elements/XButton.vue';
import { useMainStore } from '@/stores/mainStore';
import DialogCreateGroup from '../dialogs/DialogCreateGroup.vue';

var mainStore;

export default {
	name: 'HbsGrouplist',
	components: {
		XButton
	},
	methods: {
		showDialog_groupCreate() {
			console.log(mainStore.root);
			mainStore.root.showDialogWindow(DialogCreateGroup)
		}
	},
	setup() {
		mainStore = useMainStore();
	},
	mounted() {
	}
}
</script>

<style scoped>
</style>
