<template>
    <div class="router-view-container" id="rvTasks"></div>
    <div class="groupList_header">
        <div class="groupList_headerContent">Tasks</div>
        <div class="groupList_headerBackground"></div>
    </div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore'
const headerTitle = "Задачи";
var mainStore;

export default {
	name: 'RvTasks',
	mounted() {
		mainStore = useMainStore();
		mainStore.currentRightHeaderTitle = headerTitle;
		console.log(mainStore.currentRightHeaderTitle);
	},
}
</script>

<style scoped>
</style>
