
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
import { ref, createApp } from 'vue'
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

function rtc_onSessionDescription(config) {
	console.log('Remote description received: ', config);
	var peer_id = config.peer_id;
	/*
	var peer = mainStore.rtc.peerList.find(i => i.user_id == peer_id);
	if (peer == null) {
		console.log("TARGET PEER IS NULL...");
		return;
	}
	*/
	axios.get(location.protocol+"//"+location.hostname+":7070/api/users/getById/"+peer_id, {withCredentials: true})
	.then(res => {
		var remote_description = config.session_description;
		console.log(config.session_description);
		var desc = new RTCSessionDescription(remote_description);
		var peer, peer_connection;
		if (remote_description.type == "offer") { // OFFER
			peer_connection = new RTCPeerConnection(
				{"iceServers": configuration.iceServers},
				{"optional": [{"DtlsSrtpKeyAgreement": true}]}
			);
			peer = {
				user_id: peer_id,
				userInformation: res.data,
				peerConnection: peer_connection,
				srcObject: null,
				volume: 1
			};
			mainStore.rtc.peerList.push(peer);
			let stream = mainStore.rtc.callPeerYou;
			let tracks = stream.getTracks();
			console.log("ADDING A STREAM YO", stream, tracks);
			for (let i of tracks) peer_connection.addTrack(i, stream);
			rtc_hookPeerConnectionEvents(peer);
		}
		else { // ANSWER
			peer = mainStore.rtc.peerList.find(i => i.user_id == peer_id);
			peer_connection = peer.peerConnection;
		}
		console.log("Description Object: ", desc);
		peer.peerConnection.setRemoteDescription(desc, 
			function() {
				console.log("setRemoteDescription succeeded");
				if (remote_description.type == "offer") {
					console.log("Creating answer");
					peer.peerConnection.createAnswer(
						function(local_description) {
							console.log("Answer description is: ", local_description);
							peer.peerConnection.setLocalDescription(local_description,
								function() {
									let dataToSend = JSON.stringify(
											["relaySessionDescription", 
											{peer_id: peer_id, session_description: local_description}]
									);
									console.log("relaySessionDescription 1", dataToSend);
									ws.send(dataToSend);
									console.log("Answer setLocalDescription succeeded");
								},
								function() { alert("Answer setLocalDescription failed!"); }
							);
						},
						function(error) {
							console.log("Error creating answer: ", error);
							console.log(peer);
						});
				}
			},
			function(error) {
				console.log("setRemoteDescription error: ", error);
			}
		);
	})
	.catch(err => {
		console.log(err);
	})
}

function rtc_hookPeerConnectionEvents(peer) {
	let peer_connection = peer.peerConnection;
	let peer_id = peer.user_id;
	peer_connection.onicecandidate = function(event) {
		if (event.candidate) {
			let dataToSend = JSON.stringify(['relayICECandidate', {
				'peer_id': peer_id, 
				'ice_candidate': {
					'sdpMLineIndex': event.candidate.sdpMLineIndex,
					'candidate': event.candidate.candidate
				}
			}]);
			//console.log("ICE CANDIDATE", dataToSend);
			ws.send(dataToSend);
		}
	}
	peer_connection.ontrack = function(event) {
		console.log("SETTING PEER SRCOBJECT", peer.srcObject, event);
		peer.srcObject = event.streams[0];
		console.log("ontrack", event);
		/*
		let vid = document.createElement('video');
		vid.autoplay = true;
		vid.style.width = "600px";
		vid.style.height = "400px";
		vid.srcObject = event.streams[0];
		ROOT.value.appendChild(vid);
		*/
	}
}

function rtc_onAddPeer(peer_id) {
	console.log('Signaling server said to add peer:', peer_id);
	if (peer_id == mainStore.currentUser.id) {
		console.log("Peer ID is the same as current user.");
		return;
	}
	var peer = mainStore.rtc.peerList.find(i => i.user_id == peer_id);
	if (peer) {
		/* This could happen if the user joins multiple channels where the other peer is also in. */
		console.log("Already connected to peer ", peer_id);
		return;
	}
	axios.get(location.protocol+"//"+location.hostname+":7070/api/users/getById/"+peer_id, {withCredentials: true})
		.then(res => {
			console.log(res.data);
			var peer_connection = new RTCPeerConnection(
				{"iceServers": configuration.iceServers},
				{"optional": [{"DtlsSrtpKeyAgreement": true}]}
			);
			peer = {
				user_id: peer_id,
				userInformation: res.data,
				peerConnection: peer_connection,
				srcObject: null,
				volume: 1
			};
			mainStore.rtc.peerList.push(peer);
			rtc_hookPeerConnectionEvents(peer);
			let stream = mainStore.rtc.callPeerYou;
			let tracks = stream.getTracks();
			console.log("ADDING A STREAM YO", stream, tracks);
			for (let i of tracks) peer_connection.addTrack(i, stream);
			let should_create_offer = true;
			if (should_create_offer) {
				console.log("Creating RTC offer to ", peer_id);
				peer_connection.createOffer(
					function (local_description) { 
						console.log("Local offer description is: ", local_description);
						peer_connection.setLocalDescription(local_description,
							function() { 
								let dataToSend = JSON.stringify(['relaySessionDescription', 
									{'peer_id': peer_id, 'session_description': local_description}]);
								console.log("relaySessionDescription", dataToSend);
								ws.send(dataToSend);
								console.log("Offer setLocalDescription succeeded"); 
							},
							function() { alert("Offer setLocalDescription failed!"); }
						);
					},
					function (error) {
						console.log("Error sending offer: ", error);
					});
			}
		})
		.catch(err => {
			console.error(err);
		})
}

function rtc_onIceCandidate(config) {
	var peer = mainStore.rtc.peerList.find(i => i.user_id == config.peer_id);
	if (peer != null) {
		var ice_candidate = config.ice_candidate;
		peer.peerConnection.addIceCandidate(new RTCIceCandidate(ice_candidate));
	}
	else {
		console.log("ICE CANDIDATE, COULDN'T FIND PEER WITH SPECIFIED ID");
	}
}

function rtc_onRemovePeer(peer_id) {
	console.log('Signaling server said to remove peer:', peer_id);
	console.log('Signaling server said to remove peer:', mainStore.rtc.peerList);
	let peerObjectIndex = mainStore.rtc.peerList.findIndex(i => i.user_id == peer_id)
	if (peerObjectIndex != -1) {
		mainStore.rtc.peerList[peerObjectIndex].peerConnection.close();
	}
	else {
		console.log("REMOVE PEER, COULDN'T FIND IT THOUGH")
	}
	mainStore.rtc.peerList.splice(peerObjectIndex, 1);
	//delete mainStore.rtc.peerList[peerObjectIndex];
}

function rtc_setupLocalMedia(callback, errorback) {
	if (mainStore.rtc.callPeerYou != null) {
		if (callback) callback();
		return; 
	}
	/* Ask user for permission to use the computers microphone and/or camera, 
	 * attach it to an <audio> or <video> tag if they give us access. */
	console.log("Requesting access to local audio / video inputs");
	navigator.getUserMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
	navigator.mediaDevices.getUserMedia(constraints)
		.then(function(stream) {
			mainStore.rtc.callPeerYou = stream;
			console.log("Access granted to audio/video");
			console.log(mainStore.rtc.callPeerYou);
			if (callback) callback();
		})
		.catch(function() {
			console.log("Access denied for audio/video");
			if (errorback) errorback();
		})
	}

function webSocket_turnOn(room_id) {
	let userId = mainStore.currentUser.id;
	let url = "ws://"+location.hostname+":7070/api/meetings/ws/"+room_id+"/"+userId;
	console.log(url);
	ws = new WebSocket(url);
	console.log(ws);
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
		if (pdata[0] == "relaySessionDescription") {
			rtc_onSessionDescription(pdata[1]);
		}
		else if (pdata[0] == "addPeer") {
			rtc_onAddPeer(pdata[1]);
		}
		else if (pdata[0] == "removePeer") {
			rtc_onRemovePeer(pdata[1]);
		}
		else if (pdata[0] == "iceCandidate") {
			rtc_onIceCandidate(pdata[1]);
		}
	}
	ws.onopen = () => {
	};
	ws.onclose = () => {
	};
}

// Call start() to initiate.
async function _startRTC(room_id) {
	try {
		rtc_setupLocalMedia(function() {
			console.log("Turning on the websocket");
			webSocket_turnOn(room_id);
			/*
			axios.get(location.protocol+"//"+location.hostname+":7070/api/meetings/getRoomById/"+room_id,
				{withCredentials: true})
			.then(res => {
				console.log("Get meeting room ->", res.data);
				for (let i of res.data.userlist) {
					rtc_onAddPeer(i);
				}
			})
			.catch(err => {
				console.log("Get meeting room ->", err);
				// NO MEETING, SHOW THE START MEETING BUTTON
				mainStore.header.buttonSet.methods.setActiveMeeting(null);
			});
			*/
		});
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
			mainStore = useMainStore();
			mainStore.root = {
				currentDialogWindowApp: null,
				showDialogWindow: (dialogFragment, _props = {}) => {
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
					mainStore.root.currentDialogWindowApp = dialog;
					dialog.mount(dialogWrapper.value);
				},
				closeDialogWindow: () => {
					console.log("UNMOUNTING DIALOG WINDOW");
					if (mainStore.root.currentDialogWindowApp != null) mainStore.root.currentDialogWindowApp.unmount();
					mainStore.root.currentDialogWindowApp = null;
				}
			};
			mainStore.rtc = {
				startRTC(room_id) {
					console.log("STARTING RTC");
					_startRTC(room_id, true);
				},
				peerList: [/*{
					user_id: 100,
					userInformation: {id: 100, handle: "uwu", visible_name: "uwuman", avatar_fileid: 915915},
					peerConnection: null,
					//videoStream: null,
					//audioStream: null,
					srcObject: null,
					volume: 0.8
				}*/]
			};
			console.log(rightMainHeader);
			mainStore.header = {
				title: "",
				buttonSet: null
			};
			mainStore.currentFolderId = -1;
			console.log('+++++++++++++++++++++++++++');
			console.log(mainStore.root);
			console.log(mainStore.currentUser);
			console.log('+++++++++++++++++++++++++++');

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
	#main {
		max-width: 100%;
		max-height: 100%;
	}

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
		flex-shrink: 1;
		min-height: 0;
	}

	#bottombar {
		height: 64px;
		width: 100%;
	}

	.no-shrink-flex {
		flex-shrink: 0;
		display: flex;
	}

	.dialogWrapper {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		z-index: 80;
		position: fixed;
		top: 0;
		left: 0;
		transition: 0.3s ease;
	}
	
	.dialogWrapper:not(:empty) {
		background: #0004;
		backdrop-filter: blur(12px);
	}

	.dialogWrapper:empty {
		pointer-events: none;
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