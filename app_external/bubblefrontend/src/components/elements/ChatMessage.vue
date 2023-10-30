<template>
	<div class="chatMessage">
		<div class="chatMessage_meta">
			<div class="chatMessage_avatar"></div>
			<div class="chatMessage_name">{{ message_object.sender.name }}</div>
			<div class="chatMessage_timeSent">{{ message_object.time }}</div>
		</div>
		<div class="chatMessage_content">
			{{ message_object.content }}
		</div>
	</div>
</template>

<script>
	export default {
		name: 'ChatMessage',

		props: {
			message_object: {
				type: Object
			},
		}
	}
</script>

<style scoped>
.chatMessage {
	background: #eee;
	border-radius: 6px;
	padding: 12px;
	width: fit-content;
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