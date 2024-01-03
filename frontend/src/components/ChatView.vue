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
const userList = ref([]);

var ws;

function webSocket_turnOn(chat_id) {
	//ws = new WebSocket("ws://192.168.0.3/ws");
	ws = new WebSocket("ws://localhost:7070/api/messaging/ws/"+chat_id);
	ws.onmessage = (event) => {
		console.log("WEBSOCKET MESSAGE:", event.data);
		refresh(chat_id);
	};
	ws.onopen = () => {
	};
	ws.onclose = () => {
	};
}
/*
function webSocket_turnOff() {
	ws.close();
}
*/

var CHATID;

function refresh(chat_id) {
	if (ws) ws.close(); 
	if (chat_id) CHATID = chat_id;
	console.log('--------------------------')
	console.log('       CHAT REFRESH       ', CHATID)
	console.log('--------------------------')
	var mainStore = useMainStore();
	axios.post("http://127.0.0.1:7070/api/messaging/get_messages",
		{conversation_id: CHATID},
		{headers: {"X-Access-Token": mainStore.accessToken}})
	.then(res => {
		console.log(res.data);
		messageList.value = res.data;
		messageList.value.forEach(msg => {
			let tryFind = Object.keys(userList.value).find(i => i == msg.sender_id);
			if (tryFind) {
				msg["sender"] = userList.value[tryFind]
			}
			else {
				axios.get("http://127.0.0.1:7070/api/users/getById/"+msg["sender_id"], {withCredentials: true})
					.then(res2 => {
						console.log(res2.data);
						userList.value[msg["sender_id"]] = res2.data;
						msg["sender"] = userList.value[msg["sender_id"]];
					})
					.catch(err => {
						console.error(err);
						msg["sender"] = {visible_name: "Couldn't find this user."}
					})
			}
		})
		webSocket_turnOn(chat_id);
	})
	.catch(err => console.log(err));
	
}

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
	methods: {
	},
	watch: {
		chat_id: function(newValue, oldValue) {
			console.log(newValue, oldValue);
			console.log('-------------------', newValue)
			refresh(this.$props.chat_id);
		}
	},
	setup(props) {
		refresh(props.chat_id);
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
	flex-shrink: 1;
}
.chatView_messageList {
	display: flex;
	flex-direction: column;
	gap: 6px;
	flex-grow: 1;
	justify-content: flex-end;
	overflow-y: auto;
	flex-shrink: 1;
}
</style>
