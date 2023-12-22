<template>
	<div class="headerButtonSet">
		<XButton v-if="activeMeeting" icon_name="phone" appearance="outlined" @click="startMeeting()">Присоединиться к собранию</XButton>
		<XButton v-if="activeMeeting" icon_name="phone" appearance="outlined" @click="startMeeting()">Начать собрание</XButton>
		<XButton v-else icon_name="phone" appearance="outlined" @click="joinMeeting()">Начать собрание</XButton>
	</div>
</template>

<script>
//import { ref } from 'vue
import XButton from '@/components/elements/XButton.vue';
import { useMainStore } from '@/stores/mainStore';
import axios from 'axios';

var mainStore;

export default {
	name: 'HbsGroupview',
	components: {
		XButton
	},
	props: {
		activeMeeting: {
			default: null,
			type: Object
		},
		currentChannelId: {
			type: Number
		}
	},
	methods: {
		startMeeting() {
			axios.post("http://127.0.0.1:7070/api/meetings/create_room/"+mainStore.currentChannelId.value,
				{id: mainStore.currentChannelId},
				{withCredentials: true})
			.then(res => {
				console.log(res.data);

			})
			.catch(err => {
				console.log(err);
			});
			console.warn("SHOULD START MEETING HERE");
		}
	},
	setup() {
		mainStore = useMainStore();
	},
	mounted() {
	}
}
</script>

<style scoped>
</style>
