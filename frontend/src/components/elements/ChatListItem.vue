<template>
	<div class="chatListItem" @click="console.log('AAAAAAAAA', this.$route.path)" :class="[{'activeChat': this.$route.path.includes('/chats/'+chat_object.other_user.id)}]">
		<div class="chatListItemBackground"></div>
		<div class="chatListItemContent">
			<div class="chatListItem_avatar" :style="{backgroundImage: `url('${win_location.protocol}//${win_location.hostname}:7070/api/files/download/${chat_object.other_user}'')`}"></div>
			<div class="chatListItem_right">
				<div class="chatListItem_visibleName">{{ chat_object.other_user.visible_name }}</div>
				<div class="chatListItem_lastMessage">{{ lastMessage }}</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

	var route;
	var win_location = ref(window.location);

	export default {
		name: 'ChatListItem',

		props: {
			chat_object: {
				type: Object
			},
		},
		setup(props) {
			const lastMessage = ref(null);
			route = useRoute();
			axios.get(location.protocol+"//"+location.hostname+":7070/api/messaging/getLastMessage/"+props.chat_object.id, {withCredentials: true})
			.then(res => {
				console.log(res);
				lastMessage.value = res.data.text;
			})
			.catch(err => {
				console.log(err);
			})
			return {
				lastMessage,
				route,
				win_location
			}
		},
		mounted() {
		}
	}
</script>

<style scoped>
.chatListItem {
	border-radius: 6px;
	transition: 0.2s ease;
	position: relative;
	min-height: 48px;
	overflow: hidden;
	border: solid 1px #0000;
}

.chatListItemBackground {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: linear-gradient(30deg, var(--color-pale2), transparent);
	z-index: 1;
	content: "";
	opacity: 0;
	transition: 0.2s ease;
}

.activeChat {
	border-color: var(--color-primary-lighter);
	box-shadow: 0 2px 4px #0004;
}

.activeChat .chatListItemBackground {
	opacity: 1;
}

.chatListItem:hover:not(.activeChat) {
	border-color: var(--color-pale3);
	box-shadow: 0 1px 3px #0003;
}

.chatListItem:hover .chatListItemBackground {
	opacity: 0.5;
}

.chatListItemContent {
	display: flex;
	flex-direction: row;
	align-items: center;
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	z-index: 3;
	padding: 4px;
	min-height: 36px;
	gap: 6px;
}

.chatListItem_avatar {
	background-color: aliceblue;
	border-radius: 50%;
	height: 36px;
	aspect-ratio: 1;
	box-shadow: 0 1px 3px #0004;
}
.chatListItem_visibleName {
	font-weight: 500;
}
.chatListItem_lastMessage {
	font-size: 0.9em;
}
</style>