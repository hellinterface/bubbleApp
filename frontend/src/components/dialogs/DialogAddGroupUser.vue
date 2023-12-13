<template>
    <div class="gialogCreateSetup_container">
        <LabeledInput type="text" name="title" v-model="input_handle_value">Имя пользователя</LabeledInput>
        <XButton icon_name="done" @click="addUserToGroup()">Добавить</XButton>
    </div>
</template>

<script>
import { ref, toRefs } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import LabeledInput from '@/components/LabeledInput.vue'
import axios from 'axios';
import { useMainStore } from '@/stores/mainStore';

var mainStore;
const input_handle_value = ref("");
var group_id_ref = ref("");

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
            console.log(group_id_ref.value);
            console.log(input_handle_value.value, this.group_id);
            axios.post("http://127.0.0.1:7070/api/groups/add_user_to_group",
            {user_handle: input_handle_value.value, group_id: this.group_id},
            {headers: {"X-Access-Token": mainStore.accessToken}})
            .then(res => {
                console.log(res);
            })
            .catch(err => console.log(err));
        }
    },
	mounted() {
        console.warn("MOUNTED DIALOG FRAGMENT");
        console.log(this.group_id);
        console.log(this.$props);
	},
    setup(props) {
        input_handle_value.value = "";
        mainStore = useMainStore();
        console.warn("SETUP DIALOG FRAGMENT");
        group_id_ref = toRefs(props).group_id;
        return {
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
