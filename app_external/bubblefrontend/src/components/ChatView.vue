<template>
	<div class="chatView">
		<div class="chatView_messageList">
			<ChatMessage v-for="msg in messageList" :key="msg.id" :message_object="msg"></ChatMessage>
		</div>
		<div class="chatView_inputContainer">
			<ChatInput :chat_type="$props.chat_type" :chat_id="$props.chat_id"></ChatInput>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios';
import ChatMessage from './elements/ChatMessage.vue'
import ChatInput from './elements/ChatInput.vue';
import { useMainStore } from '@/stores/mainStore';

/*
const messageList = ref([
	{id: "123", content: "test123", sender: {name: "user1"}, time: "12:30"},
	{id: "456", content: "this is a message content", sender: {name: "user2"}, time: "16:40"},
]);

const messageList = ref([
	{id: "123", text: "test123", user_id: 1, time: 1701104743},
	{id: "456", text: "this is a message content", user_id: 1, time: 1701104743},
]);
*/
const messageList = ref([]);

export default {
	name: 'ChatView',
	components: {
		ChatMessage,
		ChatInput
	},
	props: {
		chat_id: {
			default: 0,
			type: Number
		},
		chat_type: {
			default: "channel",
			type: String
		}
	},
	watch: {
		chat_id: function(newValue, oldValue) {
			console.log(newValue, oldValue);
			console.log('-------------------', newValue)
			var mainStore = useMainStore();
			axios.post("http://127.0.0.1:7070/api/messaging/get_messages",
				{conversation_id: newValue},
				{headers: {"X-Access-Token": mainStore.accessToken}})
			.then(res => {
				console.log(res);
				messageList.value = res.data;
			})
			.catch(err => console.log(err));
		}
	},
	setup() {
	},
	mounted() {
	},
	data() {
		return {
			messageList
		}
	}
}
</script>

<style scoped>
.chatView {
	height: 100%;
	display: flex;
	flex-direction: column;
	gap: 6px;
}
.chatView_messageList {
	display: flex;
	flex-direction: column;
	gap: 6px;
	flex-grow: 1;
	justify-content: flex-end;
}
</style>
