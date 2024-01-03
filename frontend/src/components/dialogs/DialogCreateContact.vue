<template>
	<div class="gialogCreateContact_container">
		<div class="errorMessage"> </div>
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
//import { useMainStore } from '@/stores/mainStore';

var mainStore;
const input_handle_value = ref("");

export default {
	name: 'DialogCreateContact',
	components: {
		XButton,
		LabeledInput
	},
	methods: {
		createContact() {
			axios.get("http://127.0.0.1:7070/api/users/getByHandle/"+input_handle_value.value,
			{withCredentials: true})
			.then(res => {
				console.log(res);
				mainStore.currentUser.contacts.push(res.data.id);
				axios.post("http://127.0.0.1:7070/api/users/update",
					{contacts: mainStore.currentUser.contacts},
					{withCredentials: true})
				.then(res => {
					console.log(res);
					mainStore.currentUser = res.data;
				})
				.catch(err => console.log(err));

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
			input_handle_value
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
