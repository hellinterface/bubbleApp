<template>
	<div class="contextMenu" ref="CONTAINER" v-click-away="hide()">
		<div class="contextMenuContent">
			<ContextMenuEntry v-for="entry in object" :key="entry.text" @click.left.prevent="entry.onclick">{{ entry.text }}</ContextMenuEntry>
		</div>
	</div>
</template>

<script>
	import { ref } from 'vue'
	import ContextMenuEntry from './ContextMenuEntry.vue'
	export default {
		name: 'ContextMenu',
		components: {
			ContextMenuEntry
		},
		props: {
		},
		setup() {
			const CONTAINER = ref(null);
			return {
				CONTAINER
			}
		},
		methods: {
			test() {
				console.log("CONTEXTMENUTEST");
			},
			show() {
				//this.CONTAINER.classList.add('visible');
			},
			hide() {
				//this.CONTAINER.classList.remove('visible');
			}
		},
		data() {
			const object = ref([
				{ text: "testease", onclick: () => {console.log("TESTERASE")} }
			]);
			return {
				object
			}
		}
	}
</script>

<style scoped>
.contextMenu {
	position: fixed;
	display: flex;
	flex-direction: column;
	background: #fff;
	border: solid 1px red;
	border-radius: 6px;
	box-shadow: 0 4px 8px #0006;
	padding: 8px;
	z-index: 2000;
	top: 100px;
	left: 100px;
	width: 200px;
	height: 300px;
}
.contextMenu:not(.visible) {
	opacity: 0;
	pointer-events: none;
}
</style>