
<template>
	<div id="appContainer" ref="ROOT">
		<MqResponsive target="md+" class="no-shrink-flex">
			<div id="sidebar">
				<!--<button @click="() => showDialogWindow()">Показать диалоговое окно</button>-->
				<SidebarMain></SidebarMain>
			</div>
		</MqResponsive>
		<div id="rightSide">
			<RightMainHeader ref="rightMainHeader" :currentTitle="mainStore.header.title" :buttonSet="mainStore.header.buttonSet"></RightMainHeader>
			<div id="rightSide_mainContainer">
				<router-view></router-view>
			</div>
		</div>
		<MqResponsive target="sm-">
			<div id="bottombar">
				<BottombarMain></BottombarMain>
			</div>
		</MqResponsive>
	</div>
	<ContextMenu ref="contextMenu"></ContextMenu>
	<div class="dialogWrapper" ref="dialogWrapper"></div>
</template>

<script>
import { inject, ref, createApp } from 'vue'
import axios from 'axios';
import SidebarMain from '@/components/sidebar/Sidebar.vue'
import RightMainHeader from '@/components/RightMainHeader.vue'
import BottombarMain from '@/components/bottombar/Bottombar.vue'
import { MqResponsive } from 'vue3-mq'
import { useRouter, useRoute } from 'vue-router'
import { useMainStore } from '@/stores/mainStore'
import ContextMenu from '@/components/contextmenu/ContextMenu.vue'
import DialogWindow from '@/components/DialogWindow.vue'

const ROOT = ref(null);
const dialogWrapper = ref(null);
const rightMainHeader = ref(null);
var mainStore;
	
var ws;
const constraints = {video: true, audio: true};
const configuration = {iceServers: [{urls: 'stun:stun.l.google.com:19302'}]};
var currentTargetPeer = -1;

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
	mainStore.rtc.peerList.value.find(i => i.user_id == currentTargetPeer).peerConnection = object;
	
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
	mainStore.rtc.callPeerYou.srcObject = stream;
	//callPeerElement_you.value.setSrcObject(stream);

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
	mainStore.rtc.peerList.value.find(i => i.user_id == currentTargetPeer).srcObject = event.streams[0];
}    

/*
async function captureScreen() {
    let mediaStream = null;
    try {
        mediaStream = await navigator.mediaDevices.getDisplayMedia({
            video: {
                cursor: "always"
            },
            audio: true
        });
		return mediaStream;
    } catch (ex) {
        console.log("Error occurred", ex);
    }
}*/

function webSocket_turnOn() {
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
			let found = mainStore.rtc.peerList.value.find(entry => entry.user_id == currentTargetPeer && entry.peerConnection.type == "out");
			if (!found) {
				console.error("COULD NOT FIND PEER CONNECTION TO WRITE AN ANSWER IN");
				return;
			}
			console.warn(pdata);
			found.peerConnection.peerConnection.setRemoteDescription(pdata[1].desc).then(() => console.error("ANSWERED!!!!!!!!!!"));
		}
		else if (pdata[0] == "RTC_Candidate") {
			console.warn("ICE_CANDIDATE", pdata);
			let found = mainStore.rtc.peerList.value.find(entry => entry.user_id == pdata[1].targetPeer);
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

// Call start() to initiate.
async function _startRTC(target_id, addStreams = false) {
	try {
		webSocket_turnOn();
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

	export default {
		name: 'App',
		components: {
			ContextMenu,
			MqResponsive,
			SidebarMain,
			BottombarMain,
			RightMainHeader,
		},
		methods: {},
		setup() {
			axios.defaults.withCredentials = true;
			console.log("===", axios.defaults.withCredentials);
			const defaultUser = {"handle": "NOT_LOGGED_IN", "visible_name": "! АНОН !", "email": "no_email"};
			mainStore = useMainStore();

			const $cookies = inject('$cookies');
			let token = $cookies.get('access_token');
			console.log(token);
			mainStore.root = {
				showDialogWindow(dialogFragment, _props = {}) {
					console.log("WOOOOOOOOOOOOOOOOOOOOOOOOOOOOO DIALOG");
					console.log(dialogFragment);
					let propsObject = {
						fragment: dialogFragment,
						fragmentProps: _props
					}
					console.log(propsObject);
					let dialog = createApp(DialogWindow, propsObject);
					//dialog.setFragment(dialogFragment);
					console.log(dialog);
					dialog.mount(dialogWrapper.value);
				}
			};
			mainStore.rtc = {
				startRTC(target_id) {
					console.log("STARTING RTC");
					_startRTC(target_id, true);
				},
				peerList: [{
					user_id: 100,
					userInformation: {id: 100, handle: "uwu", visible_name: "uwuman", avatar_fileid: 915915},
					peerConnection: null,
					//videoStream: null,
					//audioStream: null,
					srcObject: null,
					volume: 0.8
				}]
			};
			console.log(rightMainHeader);
			mainStore.header = {
				title: "",
				buttonSet: null
			};
			mainStore.currentUser = defaultUser;
			console.log('+++++++++++++++++++++++++++');
			console.log(mainStore.root);
			console.log(mainStore.currentUser);
			console.log('+++++++++++++++++++++++++++');
			if (!token) {
				window.location.href = "/login";
				//mainStore.currentUser = defaultUser;
			}
			else {
				mainStore.accessToken = token;
				console.warn("GETTING ME");
				axios.get(location.protocol+"//"+location.hostname+":7070/api/users/me", {withCredentials: true}).then(res => {
					mainStore.currentUser = res.data;
					console.warn("ME", res);
				})
				.catch(err => {
					console.error("ME", err);
					window.location.href = "/login";
					//mainStore.currentUser = defaultUser;
				})
			}

			const router = useRouter();
			const route = useRoute();
			console.log(router, route);

			const contextMenu = ref(null);
			console.log(contextMenu);
			mainStore.contextMenu = contextMenu;
			return {
				contextMenu,
				ROOT,
				dialogWrapper
			}
		},
		mounted() {
			console.log("App.vue mounted")
		},
		data() {
			const mainStore = useMainStore();
			console.log(mainStore);
			return {
				mainStore
			}
		}
	}
</script>

<style>
	#appContainer {
		height: 100%;
		width: 100%;
		display: flex;
		max-width: 100%;
		max-height: 100%;
		padding: 6px;
		gap: 6px;
	}

	#sidebar {
		height: 100%;
		width: 15vw;
		min-width: 220px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		z-index: 20;
		flex-shrink: 0;
		gap: 6px;
	}

	#rightSide {
		flex-grow: 1;
		border-radius: 6px;
		z-index: 18;
		display: flex;
		gap: 6px;
		flex-direction: column;
		max-height: 100%;
	}

	#rightSide_mainContainer {
		flex-grow: 1;
	}

	#bottombar {
		height: 64px;
		width: 100%;
	}

	.no-shrink-flex {
		flex-shrink: 0;
		display: flex;
	}

	@media (max-width: 767px) {
		#appContainer {
			flex-direction: column;
		}
		#sidebar {
			height: 64px;
			width: 100%;
		}
		#sidebarLogo {
			display: none;
		}
	}
</style>