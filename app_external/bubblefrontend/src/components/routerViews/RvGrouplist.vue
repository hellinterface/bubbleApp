<template>
    <div class="router-view-container" id="rvGrouplist">
        <div class="groupList_list">
            <GroupCard v-for="group in groupList" :key="group.id" :group_title="group.title" @click="openGroupView(group.id)"></GroupCard>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import GroupCard from "../elements/GroupCard.vue"
import { useMainStore } from '@/stores/mainStore'
import hbsGroupList from '@/components/headerButtonSets/hbsGrouplist.vue'
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
		mainStore.currentRightHeaderButtonSet = hbsGroupList;
		mainStore.currentRightHeaderTitle = headerTitle;
		console.log(mainStore.currentRightHeaderTitle);
		console.log("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii");
        axios.get("http://127.0.0.1:7070/api/groups/list_mine",
        {headers: {"X-Access-Token": mainStore.accessToken}})
        .then(res => {
            console.log(res);
            groupList.value = res.data;
        })
        .catch(err => {
            groupList.value = [];
            console.error(err);
        });
	},
    setup() {
    },
    data() {
        return {
            groupList
        }
    },
	methods: {
		openGroupView(id) {
			console.warn("OPEN GROUP VIEW", id);
            this.$router.push("groupview/"+id);
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
