<template>
    <div class="gialogEditMessage_container">
        <ErrorMessage :message="errorMessage" v-if="errorMessage != null"></ErrorMessage>
        <LabeledInput type="textarea" name="text" v-model="input_text_value">Текст сообщения</LabeledInput>
        <XButton icon_name="done" @click="updateMessage()">Сохранить</XButton>
    </div>
</template>

<script>
import { ref, toRefs } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import LabeledInput from '@/components/LabeledInput.vue'
import axios from 'axios';
import { useMainStore } from '@/stores/mainStore';
import ErrorMessage from '../elements/ErrorMessage.vue';

var mainStore;
const input_text_value = ref("");
const message_object_ref = ref(null);
const errorMessage = ref(null);

export default {
	name: 'DialogEditMessage',
	components: {
        XButton,
        LabeledInput,
        ErrorMessage
	},
    props: {
        message_object: {
            type: Object
        }
    },
    methods: {
        updateMessage() {
            console.log(input_text_value.value);
            axios.post(location.protocol+"//"+location.hostname+":7070/api/messaging/editMessage",
            {id: this.message_object.id, text: input_text_value.value},
            {withCredentials: true})
            .then(res => {
                console.log(res);
                mainStore.root.closeDialogWindow();
            })
            .catch(err => {
                console.log(err);
                errorMessage.value = "Не удалось редактировать сообщение.";
            });
        }
    },
	mounted() {
        console.warn("MOUNTED DIALOG FRAGMENT");
        console.log(this.message_object);
        console.log(this.$props);
	},
    setup(props) {
        let propRefs = toRefs(props);
        console.log(propRefs.message_object);
        message_object_ref.value = propRefs.message_object.value;
        input_text_value.value = propRefs.message_object.value.text;
        mainStore = useMainStore();
        console.warn("SETUP DIALOG FRAGMENT");
        return {
            input_text_value,
            mainStore,
            errorMessage
        }
    },
    data() {
    }
}
</script>

<style scoped>
.gialogEditMessage_container {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
</style>
