<template>
	<div class="chatMessage" @click.right.prevent="(event) => {mainStore.contextMenu.show(event, contextMenuObject)}">
		<div class="chatMessage_meta">
			<div class="chatMessage_avatar"></div>
			<div class="chatMessage_name">{{ message_object?.sender?.visible_name ? message_object?.sender?.visible_name : "NO NAME" }}</div>
			<div class="chatMessage_timeSent">{{ convertTime(message_object.time) }}</div>
		</div>
		<div class="chatMessage_content">
			{{ message_object.text }}
		</div>
	</div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore';
import DialogEditMessage from '../dialogs/DialogEditMessage.vue';
import DialogDeleteMessage from '../dialogs/DialogDeleteMessage.vue';
var mainStore;

	export default {
		name: 'ChatMessage',

		props: {
			message_object: {
				type: Object
			},
		},
		watch: {
			message_object: function(newVal, oldVal) {
				console.log("PROP CHANGED = ", newVal, "FROM", oldVal);
			}
		},
		methods: {
			convertTime(unixTimestamp) {
				var time = new Date(unixTimestamp*1000);
				var y = time.getFullYear();
				var mo = time.getMonth()+1;
				var d = time.getDate();
				var h = time.getHours();
				var m = time.getMinutes();
				if (mo < 10) mo = '0' + mo;
				if (d < 10) d = '0' + d;
				if (h < 10) h = '0' + h;
				if (m < 10) m = '0' + m;
				return `${h}:${m} ${d}.${mo}.${y}`;
			},
			openDialogWindow_editMessage() {
				mainStore.root.showDialogWindow(DialogEditMessage, {message_object: this.message_object});
			},
			openDialogWindow_deleteMessage() {
				mainStore.root.showDialogWindow(DialogDeleteMessage, {message_object: this.message_object});
			}
		},
		setup() {
			mainStore = useMainStore();
			return {
				mainStore
			}
		},
		data() {
            return {
                contextMenuObject: [
                    {text: "Редактировать", onclick: () => {this.openDialogWindow_editMessage()}},
                    {text: "Удалить", onclick: () => {this.openDialogWindow_deleteMessage()}},
                ]
            }
		}
	}
</script>

<style scoped>
.chatMessage {
	border-radius: 6px;
	padding: 12px;
	width: fit-content;
	width: 100%;
	transition: 0.2s ease;
}
.chatMessage:hover {
	background: var(--color-pale1);
}
.chatMessage_meta {
	display: flex;
	gap: 6px;
	align-items: center;
	margin-bottom: 12px;
}
.chatMessage_avatar {
	background: plum;
	width: 36px;
	height: 36px;
	border-radius: 50%;
	box-shadow: 0 2px 4px #0004;
}
.chatMessage_name {
	font-weight: bold;
}
.chatMessage_timeSent {
	opacity: 0.8;
}
.chatMessage_content {
	margin-left: calc(36px + 6px);
}
</style>