<template>
	<div class="headerButtonSet">
		<XButton v-if="activeMeeting" icon_name="phone" appearance="outlined" @click="joinMeeting()">Присоединиться к собранию</XButton>
		<XButton v-else icon_name="phone" appearance="outlined" @click="startMeeting()">Начать собрание</XButton>
	</div>
</template>

<script>
import { ref } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import { useMainStore } from '@/stores/mainStore';
import axios from 'axios';

var mainStore;
var currentChannelId = ref(-1);
var activeMeeting = ref(null);

export default {
	name: 'HbsGroupview',
	components: {
		XButton
	},
	methods: {
		setActiveMeeting(val) {
			activeMeeting.value = val;
		},
		joinMeeting() {
			mainStore.rtc.startRTC(activeMeeting.value.id)
		},
		startMeeting() {
			axios.post("http://127.0.0.1:7070/api/meetings/create_room",
				{id: mainStore.currentChannelId},
				{withCredentials: true})
			.then(res => {
				console.log(res.data);
				mainStore.rtc.startRTC(mainStore.currentChannelId);
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
	},
	data() {
		return {
			activeMeeting,
			currentChannelId
		}
	}
}
</script>

<style scoped>
</style>
