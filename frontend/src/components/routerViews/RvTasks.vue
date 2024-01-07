<template>
	<div class="router-view-container" id="rvTasks">
		<div class="secondarySidebar">
			<div class="tasks_boardList">
				<ChannelLink v-for="board in boardList" :key="board.id" :channel_title="board.title" @click="setBoard(board)"></ChannelLink>
			</div>
			<XButton class="createBoardButton" appearance="outlined" icon_name="add" @click="showDialog_createBoard()">Создать доску</XButton>
		</div>
		<div class="routerView_mainContent">
			<TaskBoardView :board_id="board_id"></TaskBoardView>
		</div>
	</div>
</template>

<script>
import { ref, watch } from 'vue'
import { useMainStore } from '@/stores/mainStore'
import ChannelLink from '../elements/ChannelLink.vue'
import TaskBoardView from '../TaskBoardView.vue';
import XButton from '../elements/XButton.vue';
import axios from 'axios';
import DialogCreateTaskBoard from '../dialogs/DialogCreateTaskBoard.vue';
import { useRoute } from 'vue-router';

const headerTitle = "Задачи";
var mainStore;
var route;

const boardList = ref([]);
const board_id = ref(null);

export default {
	name: 'RvTasks',
    components: {
        ChannelLink,
		TaskBoardView,
		XButton
    },
	methods: {
		setBoard(boardObject) {
			this.$router.push("/tasks/"+boardObject.id);
		},
		showDialog_createBoard() {
			mainStore.root.showDialogWindow(DialogCreateTaskBoard)
		}
	},
	setup() {
		mainStore = useMainStore();
		console.log(mainStore.header.title);
		axios.get(location.protocol+"//"+location.hostname+":7070/api/tasks/getMyBoards", {withCredentials: true})
		.then(res => {
			console.log(res);
			boardList.value = res.data;
		})
		.catch(err => {
			console.log(err);
		})
		
        route = useRoute();
		watch(() => route.params, (newVal, oldVal) => {
			console.log("OH GOD IT CHANGED");
			console.log(newVal, oldVal);
			board_id.value = route.params.board_id;
		}, {immediate: true});
        return {
            boardList,
			board_id
        }
	},
	mounted() {
		mainStore.header.title = headerTitle;
	}
}
</script>

<style scoped>
	#rvTasks {
		height: 100%;
		display: flex;
		flex-direction: row;
		gap: 6px;
	}
	.secondarySidebar {
		height: 100%;
		width: 20%;
		background-color: #fff;
		box-shadow: 0 0 6px #0004;
		border-radius: 6px;
		padding: 6px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 6px;
	}
	.createBoardButton {
		font-size: 14px;
		padding: 4px;
	}
	.groupView_channelList {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.routerView_mainContent {
		flex-grow: 1;
	}
</style>
