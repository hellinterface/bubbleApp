<template>
	<div class="taskColumn" ref="ROOT" :column_id="columnObject.id">
		<div class="taskColumnTitle">
			<input type="text" class="taskColumnTitleInput" :value="columnObject.title" @blur="updateTitle()" ref="titleInput"/>
			<div class="taskColumnTitleButtons">
				<XButton appearance="small" @click="positionChange(-1)" icon_name="arrow_back"></XButton>
				<XButton appearance="small" @click="deleteColumn()" icon_name="delete"></XButton>
				<XButton appearance="small" @click="positionChange(1)" icon_name="arrow_forward"></XButton>
			</div>
		</div>
		<div class="taskColumnCardList">
			<TaskCard v-for="card in columnObject.cards" :key="card.id" :cardObject="card" @cardClickDirect="(event, component) => cardClick(event, component)" :card_id="card.id"></TaskCard>
		</div>
		<XButton icon_name="add" @click="createCard()" appearance="outlined" class="createCardButton">Создать карточку</XButton>
	</div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import TaskCard from './TaskCard.vue';
import XButton from './XButton.vue';

	export default {
		name: 'TaskColumn',
		components: {
			TaskCard,
			XButton
		},
		emits: ['cardClick', 'columnPositionXChange'],
		props: {
			columnObject: {
				type: Object
			},
		},
		methods: {
		},
		setup(props, {emit}) {
			const titleInput = ref(null);
			const columnObjectRef = ref(null);
			const ROOT = ref(null);
			function cardClick(event, component) {
				console.warn("card click");
				console.log(component);
				console.log(props.columnObject);
				let element = event.target;
				while (!element.classList.contains('taskCard') && element) {
					element = element.parentElement;
				}
				emit('cardClick', element, event, component)
			}
			function positionChange(direction) {
				emit('columnPositionXChange', ROOT.value, columnObjectRef.value, direction)
			}
			function updateColumn() {
				console.log("AIAIAIAIAI", columnObjectRef.value.title);
				axios.post(location.protocol+"//"+location.hostname+":7070/api/tasks/updateColumn",
				{id: columnObjectRef.value.id, title: columnObjectRef.value.title, position_x: columnObjectRef.value.position_x},
				{withCredentials: true})
				.then(res => {
					console.log(res);
				})
				.catch(err => {
					console.log(err);
				})
			}
			function updateTitle() {
				console.log("AIAIAIAIAI", titleInput.value);
				columnObjectRef.value.title = titleInput.value.value;
				updateColumn();
			}
			function createCard() {
				console.log({column_id: columnObjectRef.value.id, title: "Новая карточка", description: "", position_y: columnObjectRef.value.cards.length});
				axios.post(location.protocol+"//"+location.hostname+":7070/api/tasks/createCard",
				{column_id: columnObjectRef.value.id, title: "Новая карточка", description: "", position_y: columnObjectRef.value.cards.length},
				{withCredentials: true})
				.then(res => {
					console.log(res);
				})
				.catch(err => {
					console.log(err);
				})
			}
			onMounted(() => {
				columnObjectRef.value = props.columnObject;
				console.log(">>>>>>>>>>>>>", ROOT)
			});
			return {
				cardClick,
				positionChange,
				titleInput,
				columnObjectRef,
				ROOT,
				updateColumn,
				updateTitle,
				createCard
			}
		},
	}
</script>

<style scoped>
.taskColumn {
	border: solid 1px #0003;
	background: white;
	border-radius: 6px;
	height: 100%;
	min-width: 220px;
	box-shadow: 0 2px 6px #0004;
	transition: 0.2s ease;
	display: flex;
	flex-direction: column;
}
.taskColumn:hover {
	border: solid 1px #0006;
	box-shadow: 0 6px 12px #0005;
}

.taskColumnTitle {
	display: flex;
	align-items: center;
	border-bottom: solid 1px #0003;
	padding: 6px 12px;
	flex-direction: column;
	gap: 6px;
}

.taskColumnTitleButtons {
	display: flex;
	align-items: center;
	gap: 6px;
}

.taskColumnTitleInput {
	font-size: 1.2em;
	font-weight: bold;
	width: 100%;
}

.taskColumnTitleInput:not(:focus, :hover, :active) {
	border-color: transparent !important;
}


.taskColumnCardList {
	display: flex;
	flex-direction: column;
	gap: 0px;
	padding: 6px;
	flex-grow: 1;
}

.createCardButton {
	margin: 6px;
	font-size: 0.8em;
	height: 32px;
}

.taskColumn:hover .taskCardInsert {
	height: 12px;
}
</style>