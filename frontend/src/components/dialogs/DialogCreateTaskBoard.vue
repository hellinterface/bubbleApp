<template>
    <div class="gialogCreateSetup_container">
        <ErrorMessage :message="errorMessage" v-if="errorMessage != null"></ErrorMessage>
        <LabeledInput type="text" name="title" v-model="input_title_value">Название</LabeledInput>
        <XButton icon_name="done" @click="createGroup()">Создать</XButton>
    </div>
</template>

<script>
import { ref } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import LabeledInput from '@/components/LabeledInput.vue'
import axios from 'axios';
import { useMainStore } from '@/stores/mainStore';
import ErrorMessage from '../elements/ErrorMessage.vue';

var mainStore;
const errorMessage = ref(null);
const input_title_value = ref("");

export default {
	name: 'DialogCreateTaskBoard',
	components: {
        XButton,
        LabeledInput,
        ErrorMessage
	},
    methods: {
        createGroup() {
            console.log(input_title_value);
            axios.post(location.protocol+"//"+location.hostname+":7070/api/tasks/createBoard",
            {title: input_title_value.value},
            {headers: {"X-Access-Token": mainStore.accessToken}})
            .then(res => {
                console.log(res);
                mainStore.root.closeDialogWindow();
            })
            .catch(err => {
                console.log(err);
                errorMessage.value = "Не удалось создать доску."
            });
        }
    },
	mounted() {
        console.warn("MOUNTED DIALOG FRAGMENT");
	},
    setup() {
        input_title_value.value = "";
        mainStore = useMainStore();
        console.warn("SETUP DIALOG FRAGMENT");
        return {
            input_title_value,
            ErrorMessage
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
