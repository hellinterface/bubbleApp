<template>
	<div class="chatView">
		<div id="emptyBanner" v-if="!currentChatID">
			<div id="emptyBannerText">Выберите диалог или начните новый.</div>
		</div>
		<div class="chatView_messageList" ref="messageListElement">
			<ChatMessage v-for="msg in messageList" :key="msg.id" :message_object="msg"></ChatMessage>
		</div>
		<div class="chatView_inputContainer">
			<ChatInput v-if="currentChatID" :chat_type="$props.chat_type" :chat_id="$props.chat_id"></ChatInput>
		</div>
	</div>
</template>

<script>
import { ref, watch } from 'vue'
import axios from 'axios';
import ChatMessage from './elements/ChatMessage.vue'
import ChatInput from './elements/ChatInput.vue';
import { useMainStore } from '@/stores/mainStore';

var mainStore;
const messageList = ref([]);
var currentChatID = ref(null);

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


function refresh(chat_id) {
	if (ws) ws.close(); 
	if (chat_id) currentChatID.value = chat_id;
	console.log('--------------------------')
	console.log('       CHAT REFRESH       ', currentChatID.value)
	console.log('--------------------------')
	if (currentChatID.value != null && currentChatID.value != undefined) {
		axios.get(location.protocol+"//"+location.hostname+":7070/api/messaging/getMessages/"+currentChatID.value,
			{withCredentials: true})
		.then(res => {
			console.log(res.data);
			messageList.value = res.data;
			//if (this.messageListElement.value) this.messageListElement.value.scrollTop = 10000;
			/*
			messageList.value.forEach(msg => {
				let tryFind = Object.keys(userList.value).find(i => i == msg.sender_id);
				if (tryFind) {
					msg["sender"] = userList.value[tryFind]
				}
				else {
					axios.get(location.protocol+"//"+location.hostname+":7070/api/users/getById/"+msg["sender_id"], {withCredentials: true})
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
			*/
			webSocket_turnOn(chat_id);
		})
		.catch(err => {
			console.log(err);
			currentChatID.value = null;
			messageList.value = [];
		});
	}
	else {
		messageList.value = [];
	}
}

export default {
	name: 'ChatView',
	components: {
		ChatMessage,
		ChatInput
	},
	props: {
		chat_id: {
			default: undefined,
			type: Number
		},
		chat_type: {
			default: "channel",
			type: String
		}
	},
	methods: {
		refresh(chat_id) {
			refresh(chat_id)
		}
	},
	watch: {
	},
	setup(props) {
		const messageListElement = ref(null);
		mainStore = useMainStore();
		console.log(mainStore);
		currentChatID.value = null;
		watch(() => props.chat_id, (newValue, oldValue) => {
			console.log(newValue, oldValue);
			console.log('-------------------', newValue)
			refresh(newValue);
		}, {immediate: true});
		return {
			currentChatID,
			messageList,
			messageListElement
		}
	},
	mounted() {
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
	position: relative;
}
.chatView_messageList {
	display: flex;
	flex-direction: column;
	gap: 6px;
	flex-grow: 1;
	flex-shrink: 1;
	min-height: 0;
	overflow-y: auto;
}

#emptyBanner {
	position: absolute;
	display: flex;
	justify-content: center;
	align-items: center;
	flex-direction: column;
	width: 100%;
	height: 100%;
	top: 0;
	left: 0;
}
</style>
