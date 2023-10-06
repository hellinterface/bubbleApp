"use strict";

//fetch("/heya", {method: 'POST', body: "ONLINE"}).then(res => res.text()).then(res2 => console.log(res2));

var ws;
const constraints = {
	video: true,
	audio: true
};
const configuration = {
	iceServers: [{
		urls: 'stun:stun.l.google.com:19302'
	}]
};
const peerConnections = [];

function makePC(pc) {
	pc.ontrack = (event) => {
		let videoelement = document.querySelector(`#videoElements video[userid="${currentTargetPeer}"]`);
		if (!videoelement) {
			videoelement = document.createElement('video');
			videoelement.setAttribute('autoplay', '');
			videoelement.setAttribute('userid', currentTargetPeer);
			videoElements.appendChild(videoelement);
		}
		// Don't set srcObject again if it is already set.
		console.log("TRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACKKKKKKKKKKKKKKK", pc, event.streams);
		//if (videoelement.srcObject) return;
		videoelement.srcObject = event.streams[0];
		//start(currentTargetPeer);
	};
}

async function offerAnswer(targetPeer, desc, candidate) {
	try {
		if (desc) {
			// If you get an offer, you need to reply with an answer.
			if (desc.type === 'offer') {

				currentTargetPeer = targetPeer;
				let pc_in = new RTCPeerConnection(configuration);
				makePC(pc_in);
				let object_in = {
					peerConnection: pc_in,
					user_id: currentTargetPeer,
					type: "in"
				};
				peerConnections.push(object_in);
				await pc_in.setRemoteDescription(desc);
				await pc_in.setLocalDescription(await pc_in.createAnswer());
				ws.send(JSON.stringify(["RTC_Answer", {
					targetPeer: targetPeer,
					desc: pc_in.localDescription
				}]));
				//const stream = await navigator.mediaDevices.getUserMedia(constraints);
				//stream.getTracks().forEach((track) => pc.addTrack(track, stream));
				/*
				let pc_out = new RTCPeerConnection(configuration);
				makePC(pc_out);
				let object_out = {
					peerConnection: pc_out,
					user_id: currentTargetPeer,
					type: "out"
				};
				peerConnections.push(object);
				await pc_out.setLocalDescription(await pc_out.createAnswer());
				ws.send(JSON.stringify(["RTC_Answer", {
					targetPeer: targetPeer,
					desc: pc_out.localDescription
				}]));
				*/
				console.log("ANSWERING");
				console.log("ANSWERING");
				console.log("ANSWERING");
			} else if (desc.type === 'answer') {
				let found = peerConnections.find(entry => entry.user_id == currentTargetPeer);
				if (!found) {
					console.error("COULD NOT FIND PEER CONNECTION TO WRITE AN ANSWER IN");
					return;
				}
				await found.peerConnection.setRemoteDescription(desc);
				console.log("ANSWER RECIEVED");
				console.log("ANSWER RECIEVED");
				console.log("ANSWER RECIEVED");
			} else {
				console.log('Unsupported SDP type.');
			}
		} else if (candidate) {
			await pc.addIceCandidate(candidate);
		}
	} catch (err) {
		console.error(err);
	}
}

var currentTargetPeer = "USER_1";

console.log("Current location:", location.host);

function webSocket_turnOn() {
	//ws = new WebSocket("ws://192.168.0.3/ws");
	ws = new WebSocket("wss://" + location.host + "/ws");
	button_toggleWebSocket.innerText = "Подключение...";
	ws.onmessage = (event) => {
		console.log("WEBSOCKET MESSAGE:", event.data);
		let pdata = JSON.parse(event.data);
		if (pdata[0] == "connected") {

		} else if (pdata[0] == "userlist_update") {
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
		} else if (pdata[0] == "RTC_Offer") {
			console.log("OFFFFFFFFFEEEEEEEEEERRRRRRRRR");
			console.log("OFFFFFFFFFEEEEEEEEEERRRRRRRRR");
			let a = pdata[1];
			offerAnswer(a.targetPeer, a.desc, a.candidate).then(() => console.log("OFFER ANSWERED"));
		} else if (pdata[0] == "RTC_Answer") {
			let found = peerConnections.find(entry => entry.user_id == currentTargetPeer);
			console.warn("(ANSWER) SEARCHING FOR", currentTargetPeer, found);
			if (!found) {
				console.error("COULD NOT FIND PEER CONNECTION TO WRITE AN ANSWER IN");
				return;
			}
			found.peerConnection.setRemoteDescription(pdata[1].desc).then(() => console.log("ANSWERED!!!!!!!!!!", pdata[1]));
		}
		console.log("WEBSOCKET MESSAGE:", pdata);
	};
	ws.onopen = () => {
		ws.send(JSON.stringify(["connect"]));
		button_toggleWebSocket.innerText = "Прервать соединение";
	};
	ws.onclose = () => {
		button_toggleWebSocket.innerText = "Подключение WebSocket";
		userList.innerHTML = "";
	};
}

function webSocket_turnOff() {
	ws.close();
}

function toggleWebSocket() {
	if (ws?.readyState != WebSocket.OPEN) {
		webSocket_turnOn();
	} else {
		webSocket_turnOff();
	}
}

// Call start() to initiate.
async function start(target, addStreams = false) {
	try {
		// Get local stream, show it in self-view, and add it to be sent.
		currentTargetPeer = target;
		console.log("=====================================");
		console.log(currentTargetPeer);
		console.log("=====================================");

		let pc = new RTCPeerConnection(configuration);
		makePC(pc);
		let object = {
			peerConnection: pc,
			user_id: currentTargetPeer,
			type: "out"
		};
		peerConnections.push(object);

		pc.onicecandidate = ({
			candidate
		}) => ws.send(JSON.stringify(["RTC_Candidate", {
			targetPeer: currentTargetPeer,
			candidate: candidate
		}]));
		pc.onnegotiationneeded = async () => {
			// ***
			// The first step after start().
			// ***
			try {
				await pc.setLocalDescription(await pc.createOffer());
				// Send the offer to the other peer.
				ws.send(JSON.stringify(["RTC_Offer", {
					targetPeer: currentTargetPeer,
					desc: pc.localDescription
				}]));
			} catch (err) {
				console.error(err);
			}
		};
		pc.addEventListener('connectionstatechange', (event) => {
			if (pc.connectionState == "connected") return;
		});

		const stream = await navigator.mediaDevices.getUserMedia(constraints);
		stream.getTracks().forEach((track) => {
			//if (!addStreams) track.enabled = false;
			pc.addTrack(track, stream);
		});
		videoTestElement.srcObject = stream;
	} catch (err) {
		console.error(err);
	}
}