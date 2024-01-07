<template>
	<div class="gialogCreateSetup_container">
		<XButton icon_name="more" @click="openFileChooser()">Выбрать файлы</XButton>
		<FileEntry v-for="file in fileInput_fileList" :key="file.name" :fileObject="{title: file.name, size: file.size}"></FileEntry>
		<progress></progress>
		<XButton icon_name="upload" @click="uploadFiles()">Начать загрузку</XButton>
	</div>
</template>

<script>
import { ref } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import axios from 'axios';
import FileEntry from '@/components/elements/FileEntry.vue'
import { useMainStore } from '@/stores/mainStore';

var mainStore;

const fileInput = ref(document.createElement('input'));
const fileInput_fileList = ref(fileInput.value.files);

export default {
	name: 'DialogUploadFiles',
	components: {
		XButton,
		FileEntry
	},
	props: {
	},
	methods: {
		openFileChooser() {
			fileInput.value.click();
			//function startUpload() {
			//	let dataArray = new FormData();
			//	dataArray.append('file', file_input.files[0]);
			//}
		},
		uploadFiles() {
			let dataArray = new FormData();
			for (let file of fileInput_fileList.value) {
				dataArray.append('files', file);
			}
			let uploadOptions = {
				parent_folder_id: mainStore.currentFolderId,
				inheritView: true,
				inheritEdit: true
			};
			dataArray.append('upload_options', JSON.stringify(uploadOptions));
			for (var pair of dataArray.entries()) {
				console.log("FORM DATA :: ", pair[0]+ ', ' + pair[1]); 
			}
			axios.post(location.protocol+"//"+location.hostname+":7070/api/files/upload", dataArray, {onUploadProgress: progressEvent => console.log(progressEvent.loaded, progressEvent)})
			.then(res => {
				console.log(res);
			})
			.then(err => {
				console.log(err);
			})
		}
	},
	mounted() {
	},
	setup() {
		mainStore = useMainStore();
		fileInput.value.type = 'file';
		fileInput.value.multiple = 'true';
		fileInput.value.addEventListener("change", () => {
			console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
			console.log(fileInput.value.files);
			fileInput_fileList.value = [...fileInput.value.files];
		}, false);
		return {
			fileInput,
			fileInput_fileList
		}
	},
	data() {
	}
}
</script>

<style scoped>
.gialogCreateSetup_container {
	display: flex;
	flex-direction: column;
	gap: 8px;
	width: 75vw;
	height: 75vh;
}
</style>
