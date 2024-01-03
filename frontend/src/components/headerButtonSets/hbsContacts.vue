<template>
	<div class="headerButtonSet">
		<XButton icon_name="add" appearance="outlined" @click="showDialog_contactAdd()">Добавить контакт</XButton>
	</div>
</template>

<script>
//import { ref } from 'vue
import XButton from '@/components/elements/XButton.vue';
import DialogCreateContact from '@/components/dialogs/DialogCreateContact.vue'
import { useMainStore } from '@/stores/mainStore';
var mainStore;

export default {
	name: 'HbsContacts',
	components: {
		XButton
	},
	methods: {
		showDialog_contactAdd() {
			console.log(mainStore.root);
			mainStore.root.showDialogWindow(DialogCreateContact)
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
