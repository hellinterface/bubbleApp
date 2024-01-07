<template>
	<div class="headerButtonSet">
		<XButton icon_name="upload" appearance="outlined" @click="showDialog_uploadFiles()">Загрузить файлы</XButton>
		<XButton icon_name="add" appearance="outlined" @click="createFolder()">Создать папку</XButton>
	</div>
</template>

<script>
//import { ref } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import DialogUploadFiles from '@/components/dialogs/DialogUploadFiles.vue'
import { useMainStore } from '@/stores/mainStore';
import axios from 'axios';

var mainStore;

export default {
	name: 'HbsFiles',
	components: {
		XButton
	},
	methods: {
		createFolder() {
			if (mainStore.currentFolderId) {
				console.log({parent_folder_id: mainStore.currentFolderId, title: "Новая папка"});
				axios.post(location.protocol+"//"+location.hostname+":7070/api/files/createFolder",
				{parent_folder_id: mainStore.currentFolderId, title: "Новая папка"}, {withCredentials: true})
				.then(res => {
					console.log(res);
				})
				.catch(err => {
					console.log(err);
				})
			}
		},
		showDialog_uploadFiles() {
			mainStore.root.showDialogWindow(DialogUploadFiles)
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
