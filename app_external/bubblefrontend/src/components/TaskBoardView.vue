<template>
	<div class="taskBoardView">
        <TaskColumn v-for="column in columnList" :key="column.id" :column_object="column"></TaskColumn>
	</div>
</template>

<script>
import { ref } from 'vue'
import TaskColumn from '@/components/elements/TaskColumn.vue'

const columnList = ref([
    {id: "123", position_x: 0, title: "first column", cards: [
        {id: "123", position_y: 0, title: "cardtitle", description: "desc 123", color: "#89a"},
        {id: "234", position_y: 1, title: "card desc", description: "desc 123"},
        {id: "345", position_y: 2, title: "card color", color: "#aa7"},
    ]},
    {id: "234", position_x: 1, title: "second column", cards: [
    ]},
    {id: "345", position_x: 2, title: "third column", cards: [
        {id: "123", position_y: 0, title: "cardtitle", description: "desc 123", color: "#89a"},
        {id: "234", position_y: 1, title: "card desc", description: "desc 123"},
    ]},
    {id: "456", position_x: 3, title: "fourth column", cards: [
        {id: "123", position_y: 0, title: "cardtitle", description: "desc 123", color: "#89a"},
    ]},
]);

export default {
	name: 'TaskBoardView',
	components: {
        TaskColumn
	},
    setup() {
        return {
            columnList
        }
    }
}
</script>

<style scoped>
.taskBoardView {
    display: flex;
    flex-direction: row;
    height: 100%;
    gap: 6px;
    max-width: 100%;
    overflow: auto;
}
</style>
