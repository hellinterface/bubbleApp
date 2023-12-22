<template>
	<div class="router-view-container" id="rvSettings">
		<div class="secondarySidebar">
			<div class="settings_categories">
				<ChannelLink v-for="category in categoryList" :key="category.id" :channel_title="category.title"></ChannelLink>
			</div>
		</div>
		<div class="routerView_mainContent">
			<AvatarPicker></AvatarPicker>
			<LabeledInput type="text" :required="true" name="handle" v-model="inputValue_handle">Имя пользователя</LabeledInput>
			<LabeledInput type="text" :required="true" name="visible_name" v-model="inputValue_visibleName">Публичное имя</LabeledInput>
			<LabeledInput type="text" :required="true" name="email" v-model="inputValue_email">Почта</LabeledInput>
			<LabeledInput type="text" :required="false" name="password" v-model="inputValue_password">Пароль</LabeledInput>
			<LabeledInput type="text" :required="false" name="bio" v-model="inputValue_bio">О себе</LabeledInput>
			<XButton @click="saveChanges()">Сохранить</XButton>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue'
import { useMainStore } from '@/stores/mainStore'
import ChannelLink from '../elements/ChannelLink.vue'
import AvatarPicker from '../elements/AvatarPicker.vue';
import LabeledInput from '../LabeledInput.vue';
import XButton from '../elements/XButton.vue';
import { storeToRefs } from 'pinia';
const headerTitle = "Настройки";
var mainStore;

var currentUser;

var inputValue_handle = ref("");
var inputValue_visibleName = ref("");
var inputValue_email = ref("");
var inputValue_password = ref("");
var inputValue_bio = ref("");

const categoryList = ref([
	{id: "123", title: "Аккаунт"},
	{id: "456", title: "Система"},
]);

export default {
	name: 'RvSettings',
	components: {
		ChannelLink,
		AvatarPicker,
		LabeledInput,
		XButton
	},
	methods: {
		saveChanges() {
			async function sha256(message) {
				const msgBuffer = new TextEncoder().encode(message);
				const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
				const hashArray = Array.from(new Uint8Array(hashBuffer));
				const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
				return hashHex;
			}
			console.log(inputValue_handle.value, inputValue_visibleName.value);
			sha256(inputValue_password.value).then(passwordHash => {
				let objectToSend = {	
						handle: inputValue_handle.value, 
						visible_name: inputValue_visibleName.value,
						email: inputValue_email.value,
						bio: inputValue_bio.value,
				};
				if (inputValue_password.value != "") {
					objectToSend.password = passwordHash;
				}
				axios.post("http://127.0.0.1:7070/api/users/update",
					objectToSend,
					{withCredentials: true})
				.then(res => {
					console.log(res);
					mainStore.currentUser = res.data;
				})
				.catch(err => console.log(err));
			});
		}
	},
	watch: {
		currentUser(newVal, oldVal) {
			console.log(newVal, oldVal);
			inputValue_handle.value = currentUser.value.handle;
			inputValue_visibleName.value = currentUser.value.visible_name;
			inputValue_email.value = currentUser.value.email;
			inputValue_bio.value = currentUser.value.bio;
		}
	},
	setup() {
		mainStore = useMainStore();
		mainStore.header.title = headerTitle;
		console.log(mainStore.header.title);
		//console.log(storeToRefs(mainStore));
        currentUser = storeToRefs(mainStore).currentUser;
        console.warn("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO");
        console.warn(currentUser);
        console.warn(currentUser.value);
		return {
			currentUser,
			inputValue_handle,
			inputValue_visibleName,
			inputValue_email,
			inputValue_password,
			inputValue_bio,
		}
	},
	mounted() {
	},
	data() {
		return {
			categoryList
		}
	}
}
</script>

<style scoped>
	#rvSettings {
		height: 100%;
		display: flex;
		flex-direction: row;
		gap: 6px;
	}
	.secondarySidebar {
		height: 100%;
		width: 20%;
		background-color: #fff;
		box-shadow: 0 0 6px #0004;
		border-radius: 6px;
		padding: 6px;
	}
	.groupView_channelList {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.routerView_mainContent {
		flex-grow: 1;
	}
</style>
