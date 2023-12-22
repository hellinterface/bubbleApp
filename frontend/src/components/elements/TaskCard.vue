<template>
    <div class="taskCard" ref="ROOT" @mousedown="(event) => cardClickDirect(event)" @click.right.prevent="(event) => {mainStore.contextMenu.show(event, contextMenuObject)}">
		<div class="taskCardInsert"></div>
		<div class="taskCardContainer" ref="CONTAINER">
			<div class="taskCardTitle">{{ cardObject.title }}</div>
			<div class="taskCardDescription" v-if="cardObject.description">{{ cardObject.description }}</div>
		</div>
    </div>
</template>

<script>
	import { useMainStore } from '@/stores/mainStore';
	import { ref, toRefs, onMounted } from 'vue';
	var mainStore;
	var card_object;
	
	export default {
		name: 'TaskCard',
		props: {
			cardObject: {
				type: Object
			},
		},
		emits: ['cardClickDirect'],
		methods: {
			fuck() {

			}
		},
		setup(props, {emit}) {
			mainStore = useMainStore();
			const ROOT = ref(null);
			const CONTAINER = ref(null);
			card_object = toRefs(props).cardObject;
			onMounted(() => {
				console.log(ROOT.value);
				if (card_object.value?.color) {
					CONTAINER.value.style.background = card_object.value.color;
				}
			});
			function cardClickDirect(event) {
				emit('cardClickDirect', event, this)
			}
			return {
				ROOT,
				CONTAINER,
				mainStore,
				cardClickDirect,
				card_object
			}
		},
		data() {
            return {
                contextMenuObject: [
                    {text: "Details", onclick: () => {console.log("DETAILS CARD")}},
                    {text: "Delete", onclick: () => {console.log("DELETE CARD")}}
                ]
            }
		}
	}
</script>

<style scoped>
.taskCard {
	display: block;
	user-select: none;
	width: 100%;
	transition: 0.15s ease-in-out;
}

.taskCardContainer {
	display: block;
	padding: 8px;
	border-radius: 6px;
	text-align: left;
	font-size: 13px;
	width: 100%;
	box-sizing: border-box;
	box-shadow: 0 2px 6px #0004;
	transition: 0.15s ease-in-out;
	margin: 0 auto;
	background-color: #79e;
	color: white;
}

.taskCardTitle {
	font-weight: bold;
}


.taskCardInsert {
	display: block;
	position: relative;
	box-sizing: border-box;
	width: 100%;
	height: 6px;
	transition: 0.1s ease-in-out;
	opacity: 0;
}

.taskCardInsert::before {
	content: '';
	display: block;
	position: absolute;
	width: calc(100% - 12px);
	height: calc(100% - 12px);
	margin: 3px;
	top: 0;
	left: 0;
	background: #67f4;
	border: dotted 2px #45f6;
	border-radius: 6px;
	transform: 0.15s ease-out;
}
.card-dragging {
	position: absolute;
	transition: none;
	z-index: 30;
	pointer-events: none;
	/*width: 240px !important;*/
}
.card-dragging .taskCardInsert {
	height: 0 !important;
}
.card-dragging .taskCardContainer {
	width: 240px !important;
	box-shadow: 0 8px 24px #0006;
}
</style>

<style>

body.dragging .taskCard:hover .taskCardInsert {
	height: 64px;
	opacity: 1 !important
}

</style>