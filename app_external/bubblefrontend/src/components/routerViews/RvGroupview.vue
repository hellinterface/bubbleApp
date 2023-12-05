<template>
	<div class="rvGroupview">
		<div class="secondarySidebar">
			<div class="groupView_channelList">
				<ChannelLink v-for="channel in groupObject.channels" :key="channel.id" :channel_title="channel.title" @click="openChannel(channel.id)"></ChannelLink>
			</div>
			<XButton>Создать канал</XButton>
			<div class="groupView_userList">
				<GroupUserEntry v-for="user in groupObject.users" :key="user.user_id" :user_object="user"></GroupUserEntry>
			</div>
			<XButton @click="">Добавить пользователя</XButton>
		</div>
		<div class="routerView_mainContent">
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
//import CallView from '../CallView.vue';
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
		//CallView,
		ChatView,
		GroupUserEntry,
		XButton
	},
	methods: {
		openChannel(channel_id) {
			console.warn("OPENING CHANNEL")
			currentChannelId.value = channel_id;
			axios.post("http://127.0.0.1:7070/api/messaging/get_conversation_channel",
				{channel_id: currentChannelId.value},
				{headers: {"X-Access-Token": mainStore.accessToken}})
			.then(res => {
				console.log(res);
				currentChatId.value = res.data.id;
			})
			.catch(err => console.log(err));
		},
		showDialog_addUserToGroup() {
			console.log(mainStore.root);
			mainStore.root.showDialogWindow(DialogAddGroupUser, {group_id: groupObject.id})
		}
	},
	mounted() {
		mainStore = useMainStore();
		const route = useRoute();
		var group_id = route.params.group_id;
		console.warn("PARAM ID", group_id);
		axios.post("http://127.0.0.1:7070/api/groups/get_by_id",
			{id: group_id},
			{headers: {"X-Access-Token": mainStore.accessToken}})
		.then(res => {
			console.log(res);
			groupObject.value = res.data;
			mainStore.currentRightHeaderTitle = groupObject.value.title;
			this.openChannel(1);
		})
		.catch(err => console.log(err));
	},
	setup() {
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
	}
</style>
