<template>
	<div class="chatInput">
		<XButton class="chatInput_attachmentButton" icon_name="attachment"></XButton>
		<div class="chatInput_fieldContainer">
			<input type="text" class="chatInput_field" ref="chatInputField" @keydown="event => onKeyDown(event)">
		</div>
		<XButton class="chatInput_sendButton" icon_name="send" @click="sendMessage()"></XButton>
	</div>
</template>

<script>
	import XButton from './XButton.vue';
	import { ref } from 'vue';
	import axios from 'axios';
	//import { useMainStore } from '@/stores/mainStore';

	const chatInputField = ref(null);

	export default {
		name: 'ChatInput',
		components: {
			XButton
		},
		props: {
			chat_id: {
				type: Number
			},
			chat_type: {
				type: String
			}
		},
		methods: {
			onKeyDown(event) {
				console.log(event, event.key);
				if (event.key == "Enter") {
					this.sendMessage();
				}
			},
			sendMessage() {
				//var mainStore = useMainStore();
				// recipient_id: this.recipient_id,
				var objectToSend = {conversation_id: this.chat_id, conversation_type: this.chat_type,  text: chatInputField.value.value, media_ids: []};
				console.log(objectToSend);
				console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
				chatInputField.value.value = "";
				axios.post(location.protocol+"//"+location.hostname+":7070/api/messaging/sendMessage",
					objectToSend,
					{withCredentials: true})
				.then(res => {
					console.log(res);
				})
				.catch(err => console.log(err));
			}
		},
		setup() {
			return {
				chatInputField
			}
		}
	}
</script>

<style scoped>
	.chatInput {
		display: flex;
		align-items: center;
		height: 56px;
		gap: 6px;
	}
	.chatInput_attachmentButton {
		background: #ccc;
		color: #666;
		height: 100%;
		aspect-ratio: 1;
		border-radius: 6px;
	}
	.chatInput_fieldContainer {
		background-color: #fff;
		border: solid 1px #0004;
		flex-grow: 1;
		height: 100%;
		border-radius: 6px;
	}
	.chatInput_field {
		width: 100%;
		height: 100%;
		border: none;
		font-size: 1.05em;
	}
	.chatInput_sendButton {
		width: 82px;
		height: 100%;
		border-radius: 6px;
	}
</style>