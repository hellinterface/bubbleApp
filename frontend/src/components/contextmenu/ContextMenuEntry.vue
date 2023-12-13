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
	border-radius: 6px;
	padding: 8px;
	position: relative;
	height: 36px;
	align-items: center;
}
.contextMenuEntry::before {
	position: absolute;
	top: 3px;
	left: 3px;
	width: calc(100% - 6px);
	height: calc(100% - 6px);
	background: var(--color-primary-lighter);
	border-radius: 4px;
	content: "";
	transition: 0.2s ease;
	opacity: 0;
}
.contextMenuEntry:hover::before {
	opacity: 0.25;
}
</style>