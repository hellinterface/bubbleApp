<template>
    <div class="gialogCreateSetup_container">
        <LabeledInput type="text" name="title" v-model="input_handle_value">Имя пользователя</LabeledInput>
        <XButton icon_name="done" @click="addUserToGroup()">Добавить</XButton>
    </div>
</template>

<script>
import { ref } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import LabeledInput from '@/components/LabeledInput.vue'
import axios from 'axios';
import { useMainStore } from '@/stores/mainStore';

var mainStore;
const input_handle_value = ref("");

export default {
	name: 'DialogAddGroupUser',
	components: {
        XButton,
        LabeledInput
	},
    props: {
        group_id: {
            type: Number
        }
    },
    methods: {
        addUserToGroup() {
            console.log(input_title_value);
            axios.post("http://127.0.0.1:7070/api/groups/add_user_to_group",
            {user_handle: input_handle_value.value, group_id: this.group_id},
            {headers: {"X-Access-Token": mainStore.accessToken}})
            .then(res => console.log(res))
            .catch(err => console.log(err));
        }
    },
	mounted() {
        console.warn("MOUNTED DIALOG FRAGMENT");
	},
    setup() {
        input_title_value.value = "";
        input_handle_value.value = "";
        mainStore = useMainStore();
        console.warn("SETUP DIALOG FRAGMENT");
        return {
            input_title_value,
            input_handle_value
        }
    },
    data() {
    }
}
</script>

<style scoped>
.gialogCreateSetup_container {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
</style>
