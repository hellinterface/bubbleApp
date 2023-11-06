<template>
	<div class="chatInput">
		<XButton class="chatInput_attachmentButton" icon_name="attachment"></XButton>
		<div class="chatInput_fieldContainer">
			<input type="text" class="chatInput_field">
		</div>
		<XButton class="chatInput_sendButton" icon_name="send"></XButton>
	</div>
</template>

<script>
	import XButton from './XButton.vue';
	export default {
		name: 'ChatInput',
		components: {
			XButton
		},
		props: {
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