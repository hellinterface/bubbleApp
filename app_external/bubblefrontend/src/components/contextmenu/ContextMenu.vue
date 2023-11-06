<template>
	<div class="contextMenu zeroMaxHeight disableTransition" ref="ROOT" v-click-away="() => hide()">
		<div class="contextMenuContent">
			<ContextMenuEntry v-for="entry in object" :key="entry.text" @click.left.prevent="() => {entry.onclick(); hide();}">{{ entry.text }}</ContextMenuEntry>
		</div>
	</div>
</template>

<script>
	import { ref, onMounted } from 'vue'
	import ContextMenuEntry from './ContextMenuEntry.vue'
	const ROOT = ref(null);
	const object = ref([
		{ text: "text", onclick: () => {} }
	]);
	export default {
		name: 'ContextMenu',
		components: {
			ContextMenuEntry
		},
		props: {
		},
		setup() {
			onMounted(() => {
				console.log(ROOT.value);
			});
			return {
				ROOT
			}
		},
		methods: {
			show(event, _object) {
				console.log(event.pageX, event.pageY);
				object.value = _object;
				ROOT.value.style.top = event.pageY + "px";
				ROOT.value.style.left = event.pageX + "px";
				ROOT.value?.classList.add('visible');
				
				ROOT.value.style.maxHeight = (36 * object.value.length + 16) + "px";
				if (!this.active) {
					setTimeout(() => {
						ROOT.value.classList.remove('disableTransition');
						ROOT.value.classList.remove('zeroMaxHeight');
					}, 1);
					this.active = true;
				}
			},
			hide() {
				ROOT.value.classList.add('zeroMaxHeight');
				setTimeout(() => {
					ROOT.value.classList.add('disableTransition');
					//CONTENT.value.innerHTML = "";
				}, 200);
				this.active = false;
				ROOT.value?.classList.remove('visible');
			}
		},
		data() {
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
	border: solid 1px var(--color-primary-lighter);
	border-radius: 6px;
	box-shadow: 0 4px 8px #0006;
	z-index: 2000;
	top: 100px;
	left: 100px;
	width: 200px;
	height: 300px;
	transition: 0.2s ease;
	overflow: hidden;
}
.contextMenu:not(.visible) {
	opacity: 0;
	pointer-events: none;
}
.contextMenuContent {
	display: flex;
	flex-direction: column;
	padding: 8px;
}
.zeroHeight {
	height: 0 !important;
	padding-top: 0 !important;
	padding-bottom: 0 !important;
}
.zeroMaxHeight {
	max-height: 0 !important;
	padding-top: 0 !important;
	padding-bottom: 0 !important;
}
.disableTransition {
	transition: none !important;
}
</style>