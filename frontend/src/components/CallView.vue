<template>
	<div class="callView">
		<div class="callView_main">
			<div class="callView_peerList">
				<CallPeer :peerObject="peer" ref="callPeerElement_you"></CallPeer>
				<CallPeer v-for="peer in peerList" :key="peer.id" :peerObject="peer"></CallPeer>
			</div>
		</div>
		<div class="callView_bottomBar stdSurface">
			<XButton icon_name="call_end">Выйти из звонка</XButton>
			<BBRouterLink to="/app/call">
				<XButton icon_name="fullscreen">На весь экран</XButton>
			</BBRouterLink>
		</div>
	</div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore';
import { ref } from 'vue'
import BBRouterLink from './BBRouterLink.vue';
import CallPeer from './elements/CallPeer.vue'
import XButton from './elements/XButton.vue';
var ws;
const constraints = {video: true, audio: true};
const configuration = {iceServers: [{urls: 'stun:stun.l.google.com:19302'}]};
var currentTargetPeer = -1;
const callPeerElement_you = ref(null);
var mainStore;

async function offerAnswer(targetPeer, desc) {
	try {
		if (desc) {
			// If you get an offer, you need to reply with an answer.
			if (desc.type === 'offer') {
				currentTargetPeer = targetPeer;
				let pc_in = await createNewRTCPeerConnection('answer', desc, true);

				console.warn(pc_in.localDescription)

				ws.send(JSON.stringify(["RTC_Answer", {targetPeer: targetPeer, desc: pc_in.localDescription}]));

				console.log("ANSWERING");
				console.log("ANSWERING");
				console.log("ANSWERING");
			}
			else {
				console.log('Unsupported SDP type.');
			}
		}
	}
	catch (err) {
		console.error(err);
	}
}

async function createNewRTCPeerConnection(localDescriptionType, remoteDescription, addStreams = false) {
	let pc = new RTCPeerConnection(configuration);

	let object = {peerConnection: pc, user_id: currentTargetPeer, type: "in"};
	if (localDescriptionType == 'answer') object.type = "in";
	else object.type = "out";
	peerList.value.find(i => i.user_id == currentTargetPeer).peerConnection = object;
	
	pc.onicecandidate = ({candidate}) => {
		console.error("!!!!!!!!!!!!!!!!!!!!!! SENDING AN ICE CANDIDATE");
		console.warn(currentTargetPeer);
		ws.send( JSON.stringify( ["RTC_Candidate", {targetPeer: currentTargetPeer, ice_candidate: candidate}] ) );
	};
	pc.ontrack = (event) => ONTRACK(event);

	if (remoteDescription) {
		console.log("==========================================");
		console.log("SETTING REMOTE DESCRIPTION TO", remoteDescription);
		console.log("==========================================");
		await pc.setRemoteDescription(remoteDescription);
	}

	const stream = await navigator.mediaDevices.getUserMedia(constraints);
	stream.getTracks().forEach((track) => {
		console.warn("GETTING A TRACK", addStreams);
		if (!addStreams) track.enabled = false;
		pc.addTrack(track, stream);
	});
	callPeerElement_you.value.setSrcObject(stream);

	if (localDescriptionType == 'answer') {
		let localDescription;
		localDescription = await pc.createAnswer();
		await pc.setLocalDescription(localDescription);
	}

	pc.onnegotiationneeded = async () => {
		// ***
		// The first step after start().
		// ***
		try {
			if (localDescriptionType != 'answer') {
				let localDescription;
				localDescription = await pc.createOffer();
				console.warn("CREATING AN OFFER");
				await pc.setLocalDescription(localDescription);
			}
			// Send the offer to the other peer.
			ws.send(JSON.stringify(["RTC_Offer", {targetPeer: currentTargetPeer, desc: pc.localDescription, part: 1}]));
		}
		catch (err) {
			console.error(err);
		}
	};
	return pc;
}

function ONTRACK(event) {
	/*
	let videoelement = document.querySelector(`#videoElements video[userid="${currentTargetPeer}"]`);
	if (!videoelement) {
		console.log("CREATING VIDEO");
		videoelement = document.createElement('video');
		videoelement.setAttribute('autoplay', '');
		videoelement.setAttribute('userid', currentTargetPeer);
		videoElements.appendChild(videoelement);
	}
	console.warn("TRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACKKKKKKKKKKKKKKK");
	console.warn(event);
	//if (videoelement.srcObject) return;
	videoelement.srcObject = event.streams[0];
	console.warn("SET SRCOBJECT");
	//start(currentTargetPeer);
	*/
	peerList.value.find(i => i.user_id == currentTargetPeer).srcObject = event.streams[0];
}

// Call start() to initiate.
async function start(target_id, addStreams = false) {
	try {
		// Get local stream, show it in self-view, and add it to be sent.
		currentTargetPeer = target_id;
		console.log("=====================================");
		console.log(currentTargetPeer);
		console.log("=====================================");
		await createNewRTCPeerConnection('offer', null, addStreams);
	}
	catch (err) {
		console.error(err);
	}
}

const peerList = ref([
	{
		user_id: 100,
		userInformation: {id: 100, handle: "uwu", visible_name: "uwuman", avatar_fileid: 915915},
		peerConnection: null,
		//videoStream: null,
		//audioStream: null,
		srcObject: null,
		volume: 0.8
	}
]);

export default {
	name: 'CallView',
	components: {
		CallPeer,
		XButton,
		BBRouterLink
	},
	methods: {
		webSocket_turnOn() {
			let userId = mainStore.currentUser.id;
			ws = new WebSocket("ws://"+location.host+"/api/meetings/ws/"+userId);
			ws.onmessage = (event) => {
				console.log("WEBSOCKET MESSAGE:", event.data);
				let pdata = JSON.parse(event.data);
				/*
				else if (pdata[0] == "userlist_update") {
					userList.innerHTML = "";
					pdata[1] = JSON.parse(pdata[1]);
					for (let id of pdata[1]) {
						let element = document.createElement('button');
						element.innerText = id;
						element.addEventListener('pointerdown', (event) => {
							event.preventDefault();
							if (event.button == 0) start(id, true);
							else start(id, false);
						});
						userList.appendChild(element);
					}
				}
				*/
				if (pdata[0] == "RTC_Offer") {
					console.log("OFFFFFFFFFEEEEEEEEEERRRRRRRRR");
					console.log("OFFFFFFFFFEEEEEEEEEERRRRRRRRR");
					let a = pdata[1];
					offerAnswer(a.targetPeer, a.desc, a.candidate).then(() => console.log("OFFER ANSWERED"));
					/*
					if (a.part == 9) {
						let pc_out = new RTCPeerConnection(configuration);
						pc_out.createOffer().then(offer => {
							pc_out.setLocalDescription(offer).then(() => {
								console.warn("SENDING OFFER PT 2");
								console.warn(offer);
								console.log( JSON.stringify(["RTC_Offer", {targetPeer: currentTargetPeer, desc: offer, part: 2}]) );
								ws.send(JSON.stringify(["RTC_Offer", {targetPeer: currentTargetPeer, desc: offer, part: 2}]));
							})
						}).then(() => {
						})
					}
					*/
				}
				else if (pdata[0] == "RTC_Answer") {
					let found = peerList.value.find(entry => entry.user_id == currentTargetPeer && entry.peerConnection.type == "out");
					if (!found) {
						console.error("COULD NOT FIND PEER CONNECTION TO WRITE AN ANSWER IN");
						return;
					}
					console.warn(pdata);
					found.peerConnection.peerConnection.setRemoteDescription(pdata[1].desc).then(() => console.error("ANSWERED!!!!!!!!!!"));
				}
				else if (pdata[0] == "RTC_Candidate") {
					console.warn("ICE_CANDIDATE", pdata);
					let found = peerList.value.find(entry => entry.user_id == pdata[1].targetPeer);
					if (!found) {
						console.error("COULD NOT FIND PEER CONNECTION TO WRITE AN ANSWER IN");
						return;
					}
					let candidate = pdata[1].ice_candidate;
					console.log(candidate);
					if (candidate) { // && found.peerConnection.remoteDescription
						console.error("ADD ICE CANDIDATE");
						found.peerConnection.peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
					}
				}
				else if (pdata[0] == "RTC_PEER_DISCONNECT") {
					let videoelement = document.querySelector(`#videoElements video[userid="${currentTargetPeer}"]`);
					if (videoelement) videoelement.remove();
				}
				console.log("WEBSOCKET MESSAGE:", pdata);
			}
			ws.onopen = () => {
			};
			ws.onclose = () => {
			};
		}
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
		start();
		return {
			callPeerElement_you
		}
	},
	mounted() {
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
