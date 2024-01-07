<template>
    <div class="router-view-container" id="rvContacts">
        <div class="contacts_list">
            <ContactCard v-for="contact in contactList" :key="contact.id" :contact_object="contact"></ContactCard>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import ContactCard from "../elements/ContactCard.vue"
import { useMainStore } from '@/stores/mainStore'
import HbsContacts from '../headerButtonSets/HbsContacts.vue';
import axios from 'axios';
const headerTitle = "Контакты";
var mainStore;

const contactList = ref([]);

export default {
	name: 'RvGrouplist',
    components: {
        ContactCard
    },
    setup() {
		mainStore = useMainStore();
        return {
            mainStore,
            contactList
        }
    },
	mounted() {
		mainStore.header.title = headerTitle;
        mainStore.header.buttonSet = HbsContacts;
		console.log(mainStore.header.title);
		console.log(mainStore.header.buttonSet);
        axios.get(location.protocol+"//"+location.hostname+":7070/api/users/getMultipleById/"+mainStore.currentUser.contacts.join(','))
        .then(res => {
            console.log(res);
            contactList.value = res.data;
        })
        .catch(err => {
            console.log(err);
        })
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
