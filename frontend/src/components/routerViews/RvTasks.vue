<template>
	<div class="router-view-container" id="rvTasks">
		<div class="secondarySidebar">
			<div class="tasks_boardList">
				<ChannelLink v-for="channel in groupList" :key="channel.id" :channel_title="channel.title"></ChannelLink>
			</div>
			<XButton class="createBoardButton" appearance="outlined" icon_name="add">Создать доску</XButton>
		</div>
		<div class="routerView_mainContent">
			<TaskBoardView></TaskBoardView>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue'
import { useMainStore } from '@/stores/mainStore'
import ChannelLink from '../elements/ChannelLink.vue'
import TaskBoardView from '../TaskBoardView.vue';
import HbsTasks from '../headerButtonSets/HbsTasks.vue';
import XButton from '../elements/XButton.vue';

const headerTitle = "Задачи";
var mainStore;

const groupList = ref([
    {id: "123", title: "board1"},
    {id: "456", title: "board2"},
]);

export default {
	name: 'RvTasks',
    components: {
        ChannelLink,
		TaskBoardView,
		XButton
    },
	setup() {
		mainStore = useMainStore();
		mainStore.header.title = headerTitle;
        mainStore.header.buttonSet = HbsTasks;
		console.log(mainStore.header.title);
	},
	mounted() {
	},
    data() {
        return {
            groupList
        }
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
