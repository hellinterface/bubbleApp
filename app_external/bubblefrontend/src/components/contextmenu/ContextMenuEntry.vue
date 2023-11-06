<template>
	<div class="contextMenuEntry">
		<slot></slot>
	</div>
</template>

<script>
	export default {
		name: 'ContextMenuEntry',
		props: {
		},
		methods: {
		}
	}
</script>

<style scoped>
.contextMenuEntry {
	display: flex;
	background: #888;
	border-radius: 6px;
	padding: 8px;
}
</style>