<template>
	<div class="router-view-container" id="rvChats">
		<div class="secondarySidebar">
			<div class="chats_chatList">
				<ChatListItem v-for="chat in chatList" :key="chat.id" :chat_object="chat" @click="setChat(chat)"></ChatListItem>
			</div>
		</div>
		<div class="routerView_mainContent">
			<ChatView ref="chatViewElement" :chat_id="chat_id"></ChatView>
		</div>
	</div>
</template>

<script>
import { ref, watch } from 'vue'
import { useMainStore } from '@/stores/mainStore'
import ChatListItem from '../elements/ChatListItem.vue'
import ChatView from '../ChatView.vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
const headerTitle = "Диалоги";
var mainStore;
var route;

const chatList = ref([]);
const chat_id = ref(null);
const chatViewElement = ref(null);

export default {
	name: 'RvChats',
	components: {
		ChatListItem,
		ChatView
	},
	props: {
		other_user_id: {
			default: null, 
			type: Number
		}
	},
	methods: {
		setChat(chatObject) {
			this.$router.push("/chats/"+chatObject.other_user.id);
			//chatViewElement.value.refresh(chatObject.id);
		}
	},
	setup(props) {
		mainStore = useMainStore();
		console.warn(props.other_user_id);
		route = useRoute();
		watch(() => route.params, (newVal, oldVal) => {
			console.log(newVal, oldVal);
			console.log("CHATS - OTHER USER ID", route.params.other_user_id);
			axios.get(location.protocol+"//"+location.hostname+":7070/api/messaging/getPersonalChatWithUser/"+route.params.other_user_id, {withCredentials: true})
			.then(res => {
				console.log(res);
				chat_id.value = res.data.id;
			})
			.catch(err => {
				console.log(err);
			})
		}, {immediate: true});
		return {
			chatList,
			chat_id,
			chatViewElement
		}
	},
	mounted() {
		axios.get(location.protocol+"//"+location.hostname+":7070/api/messaging/getMyPersonalChats", {withCredentials: true})
		.then(res => {
			console.log(res);
			chatList.value = res.data;
		})
		.catch(err => {
			console.log(err);
		})
		mainStore.header.title = headerTitle;
		mainStore.header.buttonSet = null;
		console.log(mainStore.header.title);
	}
}
</script>

<style scoped>
	#rvChats {
		height: 100%;
		display: flex;
		flex-direction: row;
		gap: 6px;
	}
	.groupView_channelList {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.routerView_mainContent {
		flex-grow: 1;
	}
	.chats_chatList {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
</style>
