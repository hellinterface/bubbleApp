<template>
    <div class="taskColumn">
		<div class="taskColumnTitle">{{ columnObject.title }}</div>
		<div class="taskColumnCardList">
			<TaskCard v-for="card in columnObject.cards" :key="card.id" :cardObject="card" @cardClickDirect="(event, component) => cardClick(event, component)"></TaskCard>
		</div>
    </div>
</template>

<script>
import TaskCard from './TaskCard.vue';
	export default {
		name: 'TaskColumn',
		components: {
			TaskCard
		},
		emits: ['cardClick'],
		props: {
			columnObject: {
				type: Object
			},
		},
		setup(props, {emit}) {
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
			return {
				cardClick
			}
		}
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
}
.taskColumn:hover {
	border: solid 1px #0006;
	box-shadow: 0 6px 12px #0005;
}

.taskColumnTitle {
	font-weight: bold;
	font-size: 1.2em;
	height: 48px;
	display: flex;
	align-items: center;
	border-bottom: solid 1px #0003;
	padding: 6px 12px;
}

.taskColumnCardList {
	display: flex;
	flex-direction: column;
	gap: 0px;
	padding: 6px;
}
</style>

<style>
.taskColumn:hover .taskCardInsert {
	height: 12px;
}
</style>