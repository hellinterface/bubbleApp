<template>
	<div class="rvGroupview">
		<div class="secondarySidebar">
			<div class="secondarySidebar_top">
				<div class="groupView_channelList">
					<ChannelLink :channel_title="'Хранилище'" @click="openFolder(groupObject.folder_id)"></ChannelLink>
				</div>
				<div class="secondarySidebarTitle">Каналы</div>
				<div class="groupView_channelList">
					<ChannelLink v-for="channel in groupObject.channels" :key="channel.id" :channel_title="channel.title" @click="openChannel(channel.id)"></ChannelLink>
				</div>
				<div class="secondarySidebarTitle">Пользователи</div>
				<div class="groupView_userList">
					<GroupUserEntry v-for="user in groupObject.users" :key="user.user_id" :user_object="user"></GroupUserEntry>
				</div>
				<div class="secondarySidebarTitle">Доски задач</div>
				<div class="groupView_channelList">
					<ChannelLink v-for="board in taskBoards" :key="board.id" :channel_title="board.title" @click="openTaskBoard(board.id)"></ChannelLink>
				</div>
			</div>
			<div class="secondarySidebar_bottom">
				<XButton appearance="outlined" icon_name="add" @click="showDialog_createChannel()">Создать канал</XButton>
				<XButton appearance="outlined" icon_name="add" @click="showDialog_addUserToGroup()">Добавить пользователя</XButton>
			</div>
		</div>
		<div class="routerView_mainContent">
			<ChatView :chat_id="currentChatId" chat_type="channel" ref="CHATVIEW"></ChatView>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue'
import { useRoute } from 'vue-router';
import { useMainStore } from '@/stores/mainStore'
import ChannelLink from '../elements/ChannelLink.vue'
import ChatView from '../ChatView.vue';
import GroupUserEntry from '../elements/GroupUserEntry.vue'
import XButton from '../elements/XButton.vue';
import DialogAddGroupUser from '../dialogs/DialogAddGroupUser.vue';
import DialogCreateChannel from '../dialogs/DialogCreateChannel.vue';
import HbsGroupview from '../headerButtonSets/HbsGroupview.vue';
var mainStore;
const currentChannelId = ref(0);
const currentChatId = ref(0);
const CHATVIEW = ref(null);
const taskBoards = ref([]);

var groupObject = ref({
	channels: [],
	title: "...",
	users: []
});

export default {
	name: 'RvGroupview',
	components: {
		ChannelLink,
		ChatView,
		GroupUserEntry,
		XButton
	},
	methods: {
		openTaskBoard(board_id) {
            this.$router.push("/tasks/"+board_id);
		},
		openFolder(folder_id) {
            this.$router.push("/files/"+folder_id);
		},
		openChannel(channel_id) {
			console.warn("OPENING CHANNEL")
			mainStore.currentChannelId = channel_id;
			console.log("SETTING CURRENT CHANNEL ID TO", channel_id);
			currentChannelId.value = channel_id;
			axios.post(location.protocol+"//"+location.hostname+":7070/api/messaging/getConversationChannel",
				{channel_id: currentChannelId.value},
				{withCredentials: true})
			.then(res => {
				console.log("Get conversation channel ->", res);
				console.log("SETTING CURRENT CHAT ID TO", res.data.id);
				currentChatId.value = res.data.id;
				CHATVIEW.value.refresh(currentChatId.value);
			})
			.catch(err => console.log("Get conversation channel ->",err));
			axios.get(location.protocol+"//"+location.hostname+":7070/api/meetings/getRoomById/"+currentChannelId.value,
				{withCredentials: true})
			.then(res => {
				console.log("Get meeting room ->", res.data);
				console.log("HBS:", mainStore.header.buttonSet);
				// ACTIVE MEETING, SHOW THE JOIN BUTTON
				console.log("Current ActiveMeeting data:", mainStore.header.buttonSet.activeMeeting);
				mainStore.header.buttonSet.methods.setActiveMeeting(res.data);
			})
			.catch(err => {
				console.log("Get meeting room ->", err);
				// NO MEETING, SHOW THE START MEETING BUTTON
				mainStore.header.buttonSet.methods.setActiveMeeting(null);
			});
		},
		showDialog_addUserToGroup() {
			console.log(mainStore.root);
			mainStore.root.showDialogWindow(DialogAddGroupUser, {group_id: groupObject.value.id})
		},
		showDialog_createChannel() {
			console.log(mainStore.root);
			mainStore.root.showDialogWindow(DialogCreateChannel, {group_id: groupObject.value.id})
		}
	},
	mounted() {
		const route = useRoute();
		var group_id = route.params.group_id;
		console.warn("PARAM ID", group_id);
		groupObject.value = {};
		axios.get(location.protocol+"//"+location.hostname+":7070/api/groups/getGroupById/"+group_id,
			{withCredentials: true})
		.then(res => {
			console.log("Get group by id ->", res);
			groupObject.value = res.data;
			mainStore.header.title = groupObject.value.title;
			mainStore.header.buttonSet = HbsGroupview;
			let primaryChannel = groupObject.value.channels.find(entry => entry.is_primary == true);
			this.openChannel(primaryChannel.id);
		})
		.catch(err => console.log(err));
		axios.get(location.protocol+"//"+location.hostname+":7070/api/tasks/getBoardsOfGroup/"+group_id,
			{withCredentials: true})
		.then(res => {
			console.log("Get boards of group ->", res);
			taskBoards.value = res.data;
		})
		.catch(err => console.log(err));
	},
	setup() {
		mainStore = useMainStore();
		mainStore.currentRouterView = this;
		groupObject.value = {};
		return {
			groupObject,
			currentChatId,
			currentChannelId,
			CHATVIEW,
			taskBoards
		}
	},
	data() {
	}
}
</script>

<style scoped>
.secondarySidebarTitle {
	font-weight: bold;
}
	.rvGroupview {
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
	}
	.secondarySidebar_bottom {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.secondarySidebar .secondarySidebar_bottom > * {
		font-size: 14px;
		padding: 4px;
		width: 100%;
	}
	.groupView_channelList {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.routerView_mainContent {
		flex-grow: 1;
		flex-shrink: 1;
		display: flex;
		flex-direction: column;
		max-height: 100%;
	}
</style>
