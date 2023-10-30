<template>
    <div class="router-view-container" id="rvContacts">
        <div class="contacts_list">
            <GroupCard v-for="group in groupList" :key="group.id" :group_title="group.title"></GroupCard>
            <GroupCard group_title="geeeee"></GroupCard>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import GroupCard from "../elements/GroupCard.vue"
import { useMainStore } from '@/stores/mainStore'
const headerTitle = "Ваши группы";
var mainStore;

const groupList = ref([
    {id: "123", title: "owo"},
    {id: "456", title: "booyea"},
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
.contacts_list {
    padding: 0 3%;
    display: grid;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 16px;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    justify-content: center;
}
</style>
