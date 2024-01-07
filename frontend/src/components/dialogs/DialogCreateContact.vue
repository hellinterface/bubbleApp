<template>
	<div class="gialogCreateContact_container">
        <ErrorMessage :message="errorMessage" v-if="errorMessage != null"></ErrorMessage>
		<LabeledInput type="text" name="handle" v-model="input_handle_value">Имя пользователя</LabeledInput>
		<XButton icon_name="done" @click="createContact()">Добавить</XButton>
	</div>
</template>

<script>
import { ref } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import LabeledInput from '@/components/LabeledInput.vue'
import axios from 'axios';
import { useMainStore } from '@/stores/mainStore';
import ErrorMessage from '../elements/ErrorMessage.vue';

const errorMessage = ref(null);

var mainStore;
const input_handle_value = ref("");

export default {
	name: 'DialogCreateContact',
	components: {
		XButton,
		LabeledInput,
		ErrorMessage
	},
	methods: {
		createContact() {
			axios.get(location.protocol+"//"+location.hostname+":7070/api/users/getByHandle/"+input_handle_value.value,
			{withCredentials: true})
			.then(res => {
				console.log(res);
				mainStore.currentUser.contacts.push(res.data.id);
				axios.post(location.protocol+"//"+location.hostname+":7070/api/users/update",
					{contacts: mainStore.currentUser.contacts},
					{withCredentials: true})
				.then(res => {
					console.log(res);
					mainStore.currentUser = res.data;
					mainStore.root.closeDialogWindow();
				})
				.catch(err => {
					console.log(err);
					errorMessage.value = "Указанного пользователя не существует."
				});

			})
			.catch(err => {
				console.log(err);
			});
		}
	},
	setup() {
		mainStore = useMainStore();
		input_handle_value.value = "";
		//mainStore = useMainStore();
		console.warn("SETUP DIALOG FRAGMENT");
		return {
			input_handle_value,
			errorMessage
		}
	},
	mounted() {
		console.warn("MOUNTED DIALOG FRAGMENT");
		console.log(this.$props);
	},
	data() {
	}
}
</script>

<style scoped>
.gialogCreateContact_container {
	display: flex;
	flex-direction: column;
	gap: 8px;
}
</style>
