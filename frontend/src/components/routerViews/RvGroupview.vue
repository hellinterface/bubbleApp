<template>
	<div class="rvGroupview">
		<div class="secondarySidebar">
			<div class="groupView_channelList">
				<ChannelLink v-for="channel in groupObject.channels" :key="channel.id" :channel_title="channel.title" @click="openChannel(channel.id)"></ChannelLink>
			</div>
			<XButton @click="showDialog_createChannel()">Создать канал</XButton>
			<div class="groupView_userList">
				<GroupUserEntry v-for="user in groupObject.users" :key="user.user_id" :user_object="user"></GroupUserEntry>
			</div>
			<XButton @click="showDialog_addUserToGroup()">Добавить пользователя</XButton>
		</div>
		<div class="routerView_mainContent">
			<CallView></CallView>
			<ChatView :chat_id="currentChatId" chat_type="channel"></ChatView>
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
import CallView from '../CallView.vue';
var mainStore;
const currentChannelId = ref(0);
const currentChatId = ref(0);

var groupObject = ref({
	channels: [],
	title: "...",
	users: []
});

export default {
	name: 'RvGroupview',
	components: {
		ChannelLink,
		CallView,
		ChatView,
		GroupUserEntry,
		XButton
	},
	methods: {
		openChannel(channel_id) {
			console.warn("OPENING CHANNEL")
			mainStore.currentChannelId = channel_id;
			currentChannelId.value = channel_id;
			axios.post("http://127.0.0.1:7070/api/messaging/get_conversation_channel",
				{channel_id: currentChannelId.value},
				{withCredentials: true})
			.then(res => {
				console.log(res);
				currentChatId.value = res.data.id;
			})
			.catch(err => console.log(err));
			axios.get("http://127.0.0.1:7070/api/meetings/get_room_by_id/"+currentChannelId.value,
				{withCredentials: true})
			.then(res => {
				console.log(res.data);
				// ACTIVE MEETING, SHOW THE JOIN BUTTON
				mainStore.header.buttonSet.activeMeeting = res.data;
			})
			.catch(err => {
				console.log(err);
				// NO MEETING, SHOW THE START MEETING BUTTON
				mainStore.header.buttonSet.activeMeeting = null;
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
		axios.post("http://127.0.0.1:7070/api/groups/get_by_id",
			{id: group_id},
			{headers: {"X-Access-Token": mainStore.accessToken}})
		.then(res => {
			console.log(res);
			groupObject.value = res.data;
			mainStore.header.title = groupObject.value.title;
			mainStore.header.buttonSet = HbsGroupview;
			let primaryChannel = groupObject.value.channels.find(entry => entry.is_primary == true);
			this.openChannel(primaryChannel.id);
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
			currentChannelId
		}
	},
	data() {
	}
}
</script>

<style scoped>
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
