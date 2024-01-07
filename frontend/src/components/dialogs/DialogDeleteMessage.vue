<template>
    <div class="gialogDeleteMessage_container">
        <ErrorMessage :message="errorMessage" v-if="errorMessage != null"></ErrorMessage>
        <div>Вы уверены?</div>
        <XButton icon_name="delete" @click="deleteMessage()" appearance="red">Удалить</XButton>
    </div>
</template>

<script>
import XButton from '@/components/elements/XButton.vue';
import axios from 'axios';
import { useMainStore } from '@/stores/mainStore';
import { ref } from 'vue';
import ErrorMessage from '../elements/ErrorMessage.vue';

var mainStore;
const errorMessage = ref(null);

export default {
	name: 'DialogDeleteMessage',
	components: {
        XButton,
        ErrorMessage
	},
    props: {
        message_object: {
            type: Object
        }
    },
    methods: {
        deleteMessage() {
            axios.post(location.protocol+"//"+location.hostname+":7070/api/messaging/deleteMessage",
            {id: this.message_object.id},
            {withCredentials: true})
            .then(res => {
                console.log(res);
                mainStore.root.closeDialogWindow();
            })
            .catch(err => {
                console.log(err);
                errorMessage.value = "Не удалось удалить сообщение.";
            });
        }
    },
	mounted() {
        console.warn("MOUNTED DIALOG FRAGMENT");
        console.log(this.message_object);
        console.log(this.$props);
	},
    setup(props) {
        console.log(props.message_object);
        mainStore = useMainStore();
        console.warn("SETUP DIALOG FRAGMENT");
        return {
            mainStore,
            errorMessage
        }
    },
    data() {
    }
}
</script>

<style scoped>
.gialogDeleteMessage_container {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
</style>
