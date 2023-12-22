<template>
    <div class="router-view-container" id="rvContacts">
        <div class="contacts_list">
            <ContactCard v-for="group in groupList" :key="group.id" :group_title="group.title"></ContactCard>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import ContactCard from "../elements/ContactCard.vue"
import { useMainStore } from '@/stores/mainStore'
import HbsContacts from '../headerButtonSets/HbsContacts.vue';
const headerTitle = "Контакты";
var mainStore;

const groupList = ref([
    {id: "123", title: "user1"},
    {id: "456", title: "user2"},
]);

export default {
	name: 'RvGrouplist',
    components: {
        ContactCard
    },
	mounted() {
		mainStore = useMainStore();
		mainStore.header.title = headerTitle;
        mainStore.header.buttonSet = HbsContacts;
		console.log(mainStore.header.title);
		console.log(mainStore.header.buttonSet);
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
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    justify-content: center;
}
</style>
