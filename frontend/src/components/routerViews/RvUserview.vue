<template>
	<div class="rvUserview">
		<div :style="{backgroundImage: `url('${win_location.protocol}//${win_location.hostname}:7070/api/files/download/${userObject.avatar_fileid}')`}"></div>
		<div>{{ userObject.visible_name }}</div>
		<div>@{{ userObject.handle }}</div>
		<div>О себе: {{ userObject.bio }}</div>
		<XButton v-if="mainStore.currentUser.contacts.includes(userObject.id)">Удалить из контактов</XButton>
		<XButton v-else-if="mainStore.currentUser.id != userObject.id">Добавить в контакты</XButton>
	</div>
</template>

<script>
import axios from 'axios';
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router';
import { useMainStore } from '@/stores/mainStore'
import XButton from '../elements/XButton.vue';
var mainStore;
var win_location = ref(window.location);

var defaultUserObject = {
	id: -1, handle: "ooo", visible_name: "owo"
}

var userObject = ref(defaultUserObject);

export default {
	name: 'RvUserview',
	components: {
		XButton
	},
	methods: {
		refresh() {

		}
	},
	mounted() {
	},
	setup() {
		const route = useRoute();
		console.log("SHIT")
		mainStore = useMainStore();
		mainStore.currentRouterView = this;
		function addContact() {
			mainStore.currentUser.contacts.push(userObject.value.id);
			axios.post(location.protocol+"//"+location.hostname+":7070/api/users/update",
				{contacts: mainStore.currentUser.contacts},
				{withCredentials: true})
			.then(res => {
				console.log(res);
			})
			.catch(err => {
				console.log(err);
			});
		}
		watch(() => route.params.user_id, (newValue, oldValue) => {
			console.log(newValue, oldValue);
			axios.get(location.protocol+"//"+location.hostname+":7070/api/users/getById/"+route.params.user_id, {withCredentials: true})
			.then(res => {
				console.log("Get user by id ->", res);
				userObject.value = res.data;
				mainStore.header.title = userObject.value.visible_name;
				mainStore.header.buttonSet = null;
			})
			.catch(err => console.log(err));
		}, {immediate: true});
		return {
			userObject,
			addContact,
			mainStore,
			win_location
		}
	},
	data() {
	}
}
</script>

<style scoped>
	.rvUserview {
		height: 100%;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
</style>
