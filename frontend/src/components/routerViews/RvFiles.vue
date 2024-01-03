<template>
	<div class="router-view-container" id="rvFiles">
		<div class="routerView_mainContent">
			<div class="rvFiles_foldersContainer">
				<FolderEntry v-for="folder in folderList" :key="folder.id" :folderObject="folder"></FolderEntry>
			</div>
			<FileEntry v-for="file in fileList" :key="file.id" :fileObject="file"></FileEntry>
		</div>
	</div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore'
import FileEntry from '@/components/elements/FileEntry.vue'
import FolderEntry from '@/components/elements/FolderEntry.vue'
import { ref } from 'vue';
const headerTitle = "Файлы";
var mainStore;

var folderList = ref([
	{id: -1, title: "FOLDER 1"},
	{id: -1, title: "FOLDER 2"},
	{id: -1, title: "FOLDER 3"},
]);

var fileList = ref([
	{id: -1, title: "FILE", size: 258295},
	{id: -1, title: "FILE", size: 258295},
	{id: -1, title: "FILE", size: 258295},
	{id: -1, title: "FILE", size: 258295},
	{id: -1, title: "FILE", size: 258295},
	{id: -1, title: "FILE", size: 258295},
]);

export default {
	name: 'RvFiles',
    components: {
		FileEntry,
		FolderEntry
    },
	setup() {
		return {
			fileList,
			folderList
		}
	},
	mounted() {
		mainStore = useMainStore();
		//mainStore.header.buttonSet = HbsFiles;
		mainStore.header.title = headerTitle;
		console.log(mainStore.header.title);
	}
}
</script>

<style scoped>
#rvCall {
    height: 100%;
}
.routerView_mainContent {
    height: 100%;
}
.rvFiles_foldersContainer {
	display: flex;
	flex-wrap: wrap;
	gap: 8px;
	margin-bottom: 8px;
}
</style>
