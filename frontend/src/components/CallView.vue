<template>
	<div class="callView">
		<div class="callView_main">
			<div class="callView_peerList">
				<CallPeer v-for="peer in peerList" :key="peer.id" :peerObject="peer"></CallPeer>
			</div>
		</div>
		<video ref="callPeerElement_you" autoplay="true" style="border: solid 4px white; border-radius: 6px; width: 640px;"></video>
		<div class="callView_bottomBar stdSurface">
			<XButton icon_name="call_end">Выйти из звонка</XButton>
			<BBRouterLink to="/call">
				<XButton icon_name="fullscreen">На весь экран</XButton>
			</BBRouterLink>
		</div>
	</div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore';
import { storeToRefs } from 'pinia';
import { ref } from 'vue'
import BBRouterLink from './BBRouterLink.vue';
import CallPeer from './elements/CallPeer.vue'
import XButton from './elements/XButton.vue';
const callPeerElement_you = ref(null);
var mainStore;

var callPeerYou = ref(null);
var peerList = ref([]);

export default {
	name: 'CallView',
	components: {
		CallPeer,
		XButton,
		BBRouterLink
	},
	methods: {
	},
	setup() {
		/*
		axios.post("http://127.0.0.1:7070/api/messaging/get_conversation_channel",
			{channel_id: currentChannelId.value},
			{headers: {"X-Access-Token": mainStore.accessToken}})
		.then(res => {
			console.log(res);
			currentChatId.value = res.data.id;
		})
		.catch(err => console.log(err));
		*/
		mainStore = useMainStore();
		peerList = ref(storeToRefs(mainStore).rtc.peerList);
		
		return {
			callPeerElement_you,
			callPeerYou
		}
	},
	mounted() {
		console.log("RTC ////////////////////////////////");
		console.log(mainStore.rtc);
		console.log("RTC ////////////////////////////////");
		callPeerYou = ref(storeToRefs(mainStore).rtc.value.callPeerYou);
		console.log(callPeerElement_you.value);
		console.log("CallPeerYou:", callPeerYou, callPeerYou.value);
		callPeerElement_you.value.srcObject = callPeerYou.value;
	},
	data() {
		return {
			peerList
		}
	}
}
</script>

<style scoped>
.callView {
	height: 100%;
	display: flex;
	flex-direction: column;
	gap: 6px;
	background: #222;
	padding: 8px;
	border-radius: 6px;
}
.callView_peerList {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 6px;
}
.callView_bottomBar {
	display: flex;
	flex-direction: row;
	justify-content: center;
	padding: 6px;
}
.callView_main {
	flex-grow: 1;
}
.callView_bottomBar {
	background: #555;
	display: flex;
	gap: 8px;
}
</style>
