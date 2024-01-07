<template>
	<div class="headerButtonSet">
		<XButton icon_name="settings" appearance="outlined" @click="showDialog_taskBoardSettings()"></XButton>
		<XButton icon_name="add" appearance="outlined" @click="createColumn()">Создать столбец</XButton>
	</div>
</template>

<script>
//import { ref } from 'vue
import XButton from '@/components/elements/XButton.vue';
import { useMainStore } from '@/stores/mainStore';
import axios from 'axios';
import DialogTaskBoardSettings from '@/components/dialogs/DialogTaskBoardSettings.vue'

var mainStore;

export default {
	name: 'HbsTasks',
	components: {
		XButton
	},
	methods: {
		showDialog_taskBoardSettings() {
			mainStore.root.showDialogWindow(DialogTaskBoardSettings, {board_id: mainStore.currentTaskBoardId})
		},
		createColumn() {
			axios.get(location.protocol+"//"+location.hostname+":7070/api/tasks/getBoardById/"+mainStore.currentTaskBoardId, {withCredentials: true})
			.then(res1 => {
				console.log(res1);
				axios.post(location.protocol+"//"+location.hostname+":7070/api/tasks/createColumn", 
				{title: "Новый столбец", position_x: res1.data.columns.length, board_id: mainStore.currentTaskBoardId}, {withCredentials: true})
				.then(res2 => {
					console.log(res2);
				})
				.catch(err2 => {
					console.log(err2);
				});
			})
			.catch(err1 => {
				console.log(err1);
			})
		}
	},
	setup() {
		mainStore = useMainStore();
		return {
			mainStore
		}
	},
	mounted() {
	}
}
</script>

<style scoped>
</style>
