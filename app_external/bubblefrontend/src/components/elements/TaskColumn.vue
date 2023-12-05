<template>
    <div class="taskColumn">
		<div class="taskColumnTitle">{{ column_object.title }}</div>
		<div class="taskColumnCardList">
			<TaskCard v-for="card in column_object.cards" :key="card.id" :card_object="card" @mousedown="(event) => cardClick(this, event)"></TaskCard>
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
			column_object: {
				type: Object
			},
		},
		setup(props, {emit}) {
			function cardClick(event) {
				console.warn("SHIT");
				emit('cardClick', event.target, event)
			}
			return {
				cardClick
			}
		}
	}
</script>

<style scoped>
.taskColumn {
	border: solid 1px #0004;
	border-radius: 4px;
    height: 100%;
	min-width: 220px;
}

.taskColumnTitle {
	font-weight: bold;
	font-size: 1.2em;
	height: 48px;
	display: flex;
	align-items: center;
	border-bottom: solid 1px #0004;
	padding: 6px 12px;
}

.taskColumnCardList {
	display: flex;
	flex-direction: column;
	gap: 6px;
	padding: 6px;
}
</style>