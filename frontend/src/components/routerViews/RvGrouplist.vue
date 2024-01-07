<template>
    <div class="router-view-container" id="rvGrouplist">
        <div class="groupList_list">
            <GroupCard v-for="group in groupList" :key="group.id" :group_object="group" @click="openGroupView(group.id)"></GroupCard>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import GroupCard from "../elements/GroupCard.vue"
import { useMainStore } from '@/stores/mainStore'
import HbsGrouplist from '@/components/headerButtonSets/HbsGrouplist.vue'
const headerTitle = "Группы";
var mainStore;

const groupList = ref([]);

export default {
	name: 'RvGrouplist',
    components: {
        GroupCard
    },
    setup() {
		mainStore = useMainStore();
        mainStore.header.buttonSet = HbsGrouplist;
		mainStore.header.title = headerTitle;
		console.log(mainStore.header.title);
		console.log(mainStore.header.buttonSet);
    },
	mounted() {
		console.log("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii");
        axios.get(location.protocol+"//"+location.hostname+":7070/api/groups/listMine", {withCredentials: true})
        .then(res => {
            console.log(res);
            groupList.value = res.data;
        })
        .catch(err => {
            groupList.value = [];
            console.error(err);
        });
	},
    data() {
        return {
            groupList
        }
    },
	methods: {
		openGroupView(id) {
			console.warn("OPEN GROUP VIEW", id);
            this.$router.push("/groupview/"+id);
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
