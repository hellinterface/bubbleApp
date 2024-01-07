<template>
	<div class="taskBoardView" ref="ROOT">
		<div id="emptyBanner" v-if="!currentBoardID">
			<div id="emptyBannerText">Выберите доску или создайте новую.</div>
		</div>
		<div class="taskBoard_columnList" v-if="currentBoardID">
			<TaskColumn v-for="column in boardObject.columns" :key="column.id" :columnObject="column" @cardClick="(element, event, component) => dragElement(element, event, component)" @columnPositionXChange="(element, object, direction) => columnPositionXChange(element, object, direction)"></TaskColumn>
		</div>
		<div class="taskBoard_cardEditorContainer" v-if="currentBoardID && selectedCardObject">
			<CardEditor :cardObject="selectedCardObject"></CardEditor>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue'
import TaskColumn from '@/components/elements/TaskColumn.vue'
import CardEditor from '@/components/elements/CardEditor.vue'
import axios from 'axios';
import { useMainStore } from '@/stores/mainStore';
import HbsTasks from '@/components/headerButtonSets/HbsTasks.vue';

/*
const columnList = ref([
	{id: "123", position_x: 0, title: "first column", cards: [
		{id: "234", position_y: 0, title: "card  title", description: "desc 123", color: "#89a", attachedFiles: [{
			id: 987, title: "some file.txt", size: 2800
			}]
		},
		{id: "345", position_y: 1, title: "card desc", description: "desc 123"},
		{id: "456", position_y: 2, title: "card color", color: "#aa7"},
	]},
	{id: "567", position_x: 1, title: "second column", cards: [
	]},
	{id: "678", position_x: 2, title: "third column", cards: [
		{id: "789", position_y: 0, title: "card  title", description: "desc 123", color: "#89a"},
		{id: "890", position_y: 1, title: "card desc", description: "desc 123"},
	]},
	{id: "90", position_x: 3, title: "fourth column", cards: [
		{id: "0", position_y: 0, title: "card __title", description: "desc 123", color: "#89a"},
	]},
]);*/

var defaultBoardObject = {title: "NULL", columns: [], users: [], groups: [], owner: {}};
const selectedCardObject = ref(null);
const boardObject = ref(defaultBoardObject);
const currentBoardID = ref(null);
var mainStore;

var ws;

function webSocket_turnOn(board_id) {
	//ws = new WebSocket("ws://192.168.0.3/ws");
	ws = new WebSocket("ws://localhost:7070/api/tasks/ws/"+board_id);
	ws.onmessage = (event) => {
		console.log("WEBSOCKET MESSAGE:", event.data);
		refresh();
	};
	ws.onopen = () => {
	};
	ws.onclose = () => {
	};
}

function refresh() {
	if (ws) ws.close();
	mainStore.currentTaskBoardId = currentBoardID.value;
    mainStore.header.buttonSet = HbsTasks;
	if (currentBoardID.value != null && currentBoardID.value != undefined) {
		axios.get(location.protocol+"//"+location.hostname+":7070/api/tasks/getBoardById/"+currentBoardID.value)
		.then(res => {
			console.log('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ');
			console.log(res);
			let data = res.data;
			data.columns = data.columns.sort((a, b) => {return (a.position_x - b.position_x)});
			for (let i in data.columns) {
				data.columns[i].cards = data.columns[i].cards.sort((a, b) => {return (a.position_y - b.position_y)});
			}
			boardObject.value = data;
			webSocket_turnOn(currentBoardID.value);
		})
		.catch(err => {
			console.log(err);
			boardObject.value = defaultBoardObject;
		})
	}
	else {
		boardObject.value = defaultBoardObject;
        mainStore.header.buttonSet = null;
	}
}

export default {
	name: 'TaskBoardView',
	components: {
		TaskColumn,
		CardEditor
	},
	props: {
		board_id: {
			type: Number
		}
	},
	watch: {
		board_id(newValue, oldValue) {
			console.log("OH YEAH NOW");
			console.log(newValue, oldValue);
			console.log('-------------------', newValue);
			currentBoardID.value = newValue;
			refresh();
		}
	},
	methods: {
		refresh() {
			refresh();
		},
		columnPositionXChange(element, columnObject, direction) {
			console.log(element, columnObject, direction);
			// element.style.backgroundColor = "red";
			// element.previousSibling.getAttribute('column_id')
			let tryFind = boardObject.value.columns.findIndex(entry => entry.id == columnObject.id);
			if (((tryFind == 0) && (direction == -1)) || (tryFind == boardObject.value.columns.length-1) && (direction == 1)) {
				console.log("Limit")
			}
			else {
				let obj1 = boardObject.value.columns[tryFind];
				console.log("OBJ1", obj1);
				obj1.position_x += direction;
				let obj2 = boardObject.value.columns[tryFind + direction];
				obj2.position_x -= direction;
				axios.post(location.protocol+"//"+location.hostname+":7070/api/tasks/updateMultipleColumns",
				[{id: obj1.id, position_x: obj1.position_x}, {id: obj2.id, position_x: obj2.position_x}],
				{withCredentials: true})
				.then(res => {
					console.log(res);
				})
				.catch(err => {
					console.log(err);
				})
			}
		},
		dragElement(drag, event, component) {
			console.log("DRAG", drag, event);
			let originalParent;
			let innerX = 0, innerY = 0;
			let first_X = 0, first_Y = 0;
			let dragStarted = false;
			dragMouseDown(event);

			let deckElements = [...this.ROOT.querySelectorAll('.taskColumn')];
			let deckCardLineElements = [];
			deckElements.forEach(element => deckCardLineElements.push(element.querySelector('.taskColumnCardList')));

			function dragMouseDown(event) {
				event.preventDefault();
				//console.log(event.target.tagName);
			
				if (event.button == 2) {
					document.onpointerup = () => onRightClick(event);
				}
				if (event.button == 0 && event.target.tagName != 'A' && !drag.deleted) {
					originalParent = drag.parentElement;
				
					let rect = drag.getBoundingClientRect();
					innerX = event.clientX - rect.left;
					innerY = event.clientY - rect.top;
					console.log(innerX, innerY);
					first_X = event.clientX;
					first_Y = event.clientY;
					dragStarted = false;
				
					document.onpointerup   = closeDragElement;
					document.onpointermove = elementDrag;
				}
			}

			function onRightClick(event) {
				event.preventDefault();
				document.onpointerup = null;
			}

			function elementDrag(event) {
				event.preventDefault();
				if (dragStarted == false && (Math.abs(first_X-event.clientX) > 8 || Math.abs(first_Y-event.clientY) > 8)) {
					drag.style.width = drag.offsetWidth + "px";
					drag.classList.add('card-dragging');
					document.body.classList.add('dragging');
					dragStarted = true;
				}

				drag.style.top  = event.clientY + "px";
				drag.style.left = event.clientX - 120 + "px";
			}

			function closeDragElement(event) {
				if (dragStarted == true) {
					let target;
					if (event.pointerType == "mouse") {
						target = event.target;
					}
					else if (event.pointerType == "touch") {
						target = document.elementFromPoint(event.clientX, event.clientY);
					}
					console.warn(event);
					console.warn(event.target);
					if (target.className == "taskColumn") {
						target.querySelector(".taskColumnCardList").appendChild(drag);
						a();
					}
					else if (target.className == "taskColumnCardList") {
						target.appendChild(drag);
						a();
					}
					else if (target.className == "taskCardInsert") {
						target.parentElement.insertAdjacentElement('beforebegin', drag);
						a();
					}
					else {
						originalParent.appendChild(drag);
					}
				}
				else {
					console.log(component);
					selectedCardObject.value = component.card_object;
				}
				drag.style.top = 'auto'; drag.style.left = 'auto';
				drag.classList.remove('card-dragging');
				document.body.classList.remove('dragging');
				drag.style.width = "100%";
			
				document.onpointermove = null;
				document.onpointerup = null;
			
			}
			function a() {
				let tryFind_new = deckCardLineElements.findIndex(entry => entry == drag.parentElement);
				let tryFind_old = deckCardLineElements.findIndex(entry => entry == originalParent);
				console.log("THE A FUNCTION");
				console.log(deckElements, deckCardLineElements, drag.parentElement, tryFind_new, tryFind_old);
				if (tryFind_new != -1 && tryFind_old != -1) {
					let card = boardObject.value.columns[tryFind_old].cards.find(i => i.id == component.card_object.id);
					let cardIndex = boardObject.value.columns[tryFind_old].cards.findIndex(i => i.id == component.card_object.id);
					card.column_id = boardObject.value.columns[tryFind_new].id;
					boardObject.value.columns[tryFind_old].cards.splice(cardIndex, 1);
					boardObject.value.columns[tryFind_new].cards.push(card);
					let listToUpdate = [];
					for (let i of boardObject.value.columns[tryFind_old].cards) {
						let index = [...deckCardLineElements[tryFind_old].children].findIndex(element => element.getAttribute("card_id") == i.id);
						if (index != -1) {
							i.position_y = index;
							listToUpdate.push({id: i.id, column_id: i.column_id, position_y: i.position_y});
						}
					}
					if (tryFind_old != tryFind_new) {
						for (let i of boardObject.value.columns[tryFind_new].cards) {
							let index = [...deckCardLineElements[tryFind_new].children].findIndex(element => element.getAttribute("card_id") == i.id);
							if (index != -1) {
								i.position_y = index;
								listToUpdate.push({id: i.id, column_id: i.column_id, position_y: i.position_y});
							}
						}
					}
					console.log(boardObject.value.columns[tryFind_old].cards, boardObject.value.columns[tryFind_new].cards)
					axios.post(location.protocol+"//"+location.hostname+":7070/api/tasks/updateMultipleCards",
					listToUpdate, {withCredentials: true})
					.then(res => {
						console.log(res);
					})
					.catch(err => {
						console.log(err);
					})
				}
			}
		}
	},
	setup() {
		const ROOT = ref(null);
		mainStore = useMainStore();
		//watch(props.board_id, , {immediate: true});
		return {
			ROOT,
			selectedCardObject,
			boardObject,
			currentBoardID,
			mainStore
		}
	},
	mounted() {
		selectedCardObject.value = null;
		currentBoardID.value = this.board_id;
		refresh();
	}
}
</script>

<style scoped>
.taskBoardView {
	display: flex;
	flex-direction: row;
	height: 100%;
	gap: 6px;
	flex-grow: 1;
}

.taskBoard_cardEditorContainer {
	height: 100%;
	flex-shrink: 0;
}

.taskBoard_columnList {
	display: flex;
	flex-direction: row;
	height: 100%;
	gap: 6px;
	max-width: 100%;
	overflow: auto;
	flex-grow: 1;
}

.taskBoardView.dragging .taskCard:hover .taskCardInsert {
	height: 64px;
	opacity: 1 !important
}

#emptyBanner {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	height: 100%;
}

@media (max-width: 900px) {
	.taskBoardView {
		flex-direction: column;
	}
	.taskBoard_cardEditorContainer {
		height: fit-content;
	}
}
</style>
