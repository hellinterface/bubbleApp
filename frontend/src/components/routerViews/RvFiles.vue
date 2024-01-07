<template>
	<div class="router-view-container" id="rvFiles">
		<div class="routerView_mainContent">
			<div class="rvFiles_folderInfo">
				<div class="rvFiles_folderInfo_title">{{folderInfo.title}}</div>
				<div class="rvFiles_folderInfo_title">Владелец: {{folderInfo.owner.visible_name}} (@{{folderInfo.owner.handle}})</div>
			</div>
			<div class="rvFiles_foldersContainer">
				<FolderEntry v-for="folder in folderContents.folders" :key="folder.id" :folderObject="folder" @click="openFolder(folder.id)"></FolderEntry>
			</div>
			<FileEntry v-for="file in folderContents.files" :key="file.id" :fileObject="file"></FileEntry>
		</div>
	</div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore'
import FileEntry from '@/components/elements/FileEntry.vue'
import FolderEntry from '@/components/elements/FolderEntry.vue'
import HbsFiles from '@/components/headerButtonSets/HbsFiles.vue'
import { ref, watch } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
const headerTitle = "Файлы";
var mainStore;
var route;

var folderInfo = ref({
	id: -1,
	title: "Null folder",
	owner: {id: -1, handle: "none", visible_name: "None"},
	share_link: "",
	users: [],
	groups: [],
});

var folderContents = ref({
	folders: [],
	files: []
});

export default {
	name: 'RvFiles',
	components: {
		FileEntry,
		FolderEntry
	},
	setup() {
		route = useRoute();
		mainStore = useMainStore();
        mainStore.header.buttonSet = HbsFiles;
		watch(() => route.params, (newVal, oldVal) => {
			console.log(newVal, oldVal);
			var folderShareLink = route.params.folder_share_link;
			console.warn("PARAM LINK", folderShareLink);
			folderContents.value = {folders: [], files: []};
			if (folderShareLink) {
				axios.get(location.protocol+"//"+location.hostname+":7070/api/files/getFolderByLink/"+folderShareLink, {withCredentials: true})
				.then(res => {
					console.log(res);
					folderInfo.value = res.data;
				})
				.catch(err => {
					console.error(err);
					axios.get(location.protocol+"//"+location.hostname+":7070/api/files/getFolderById/"+folderShareLink, {withCredentials: true})
					.then(res => {
						console.log(res);
						folderInfo.value = res.data;
					})
					.catch(err => {
						console.error(err);
					});
				});
			}
			else {
				axios.get(location.protocol+"//"+location.hostname+":7070/api/files/getFolderById/"+mainStore.currentUser.folder_id, {withCredentials: true})
				.then(res => {
					console.log(res);
					folderInfo.value = res.data;
				})
				.catch(err => {
					console.error(err);
				});
			}
		}, {immediate: true});
		return {
			folderContents,
			folderInfo
		}
	},
	mounted() {
		//mainStore.header.buttonSet = HbsFiles;
		mainStore.header.title = headerTitle;
		console.log(mainStore.header.title);
	},
	watch: {
		folderInfo(newVal, oldVal) {
			console.log("FOLDER INFO CHANGED", newVal, oldVal);
			console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", newVal.id);
			mainStore.currentFolderId = newVal.id;
			axios.get(location.protocol+"//"+location.hostname+":7070/api/files/getFolderContents/"+newVal.id, {withCredentials: true})
			.then(res => {
				console.log(res);
				folderContents.value = res.data;
			})
			.catch(err => {
				folderContents.value = {folders: [], files: []};
				console.error(err);
			});
		}
	},
	methods: {
		openFolder(id) {
            this.$router.push("/files/"+id);
			
		}
	}
}
</script>

<style scoped>
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
