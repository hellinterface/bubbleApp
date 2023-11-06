<template>
    <div class="router-view-container" id="rvGrouplist">
        <div class="groupList_list">
            <GroupCard v-for="group in groupList" :key="group.id" :group_title="group.title"></GroupCard>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import GroupCard from "../elements/GroupCard.vue"
import { useMainStore } from '@/stores/mainStore'
const headerTitle = "Группы";
var mainStore;

const groupList = ref([
    {id: "123", title: "group1"},
    {id: "456", title: "group2"},
]);

export default {
	name: 'RvGrouplist',
    components: {
        GroupCard
    },
	mounted() {
		mainStore = useMainStore();
		mainStore.currentRightHeaderTitle = headerTitle;
		console.log(mainStore.currentRightHeaderTitle);
	},
    data() {
        return {
            groupList
        }
    }
}
</script>

<style scoped>
.groupList_list {
    padding: 0 3%;
    display: grid;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 16px;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    justify-content: center;
}
</style>
