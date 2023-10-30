<template>
	<div class="chatView">
        <div class="chatView_messageList">
            <ChatMessage v-for="msg in messageList" :key="msg.id" :message_object="msg"></ChatMessage>
        </div>
        <div class="chatView_inputContainer">
            <ChatInput></ChatInput>
        </div>
	</div>
</template>

<script>
import { ref } from 'vue'
import ChatMessage from './elements/ChatMessage.vue'
import ChatInput from './elements/ChatInput.vue';

const messageList = ref([
    {id: "123", content: "test123", sender: {name: "owoman"}, time: "12:30pm"},
    {id: "456", content: "booyeah. booyeah. booyeah. booyeah. booyeah.", sender: {name: "uwuman"}, time: "16:40pm"},
]);

export default {
	name: 'ChatView',
	components: {
		ChatMessage,
        ChatInput
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
