
"use strict";

//fetch("/heya", {method: 'POST', body: "ONLINE"}).then(res => res.text()).then(res2 => console.log(res2));

var ws;
const constraints = {video: true, audio: true};
const configuration = {iceServers: [{urls: 'stun:stun.l.google.com:19302'}]};
const peerConnections = [];

async function offerAnswer(targetPeer, desc, candidate) {
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

var currentTargetPeer = "USER_1";

console.log("Current location:", location.host);

function webSocket_turnOn() {
	//ws = new WebSocket("ws://192.168.0.3/ws");
	ws = new WebSocket("ws://"+location.host+"/ws");
	button_toggleWebSocket.innerText = "Подключение...";
	ws.onmessage = (event) => {
		console.log("WEBSOCKET MESSAGE:", event.data);
		let pdata = JSON.parse(event.data);
		if (pdata[0] == "connected") {
			
		}
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
		else if (pdata[0] == "RTC_Offer") {
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
			let found = peerConnections.find(entry => entry.user_id == currentTargetPeer && entry.type == "out");
			if (!found) {
				console.error("COULD NOT FIND PEER CONNECTION TO WRITE AN ANSWER IN");
				return;
			}
			console.warn(pdata);
			found.peerConnection.setRemoteDescription(pdata[1].desc).then(() => console.error("ANSWERED!!!!!!!!!!"));
		}
		else if (pdata[0] == "RTC_Candidate") {
			console.warn("ICE_CANDIDATE", pdata);
			let found = peerConnections.find(entry => entry.user_id == pdata[1].targetPeer);
			if (!found) {
				console.error("COULD NOT FIND PEER CONNECTION TO WRITE AN ANSWER IN");
				return;
			}
			let candidate = pdata[1].ice_candidate;
			console.log(candidate);
			if (candidate) { // && found.peerConnection.remoteDescription
				console.error("ADD ICE CANDIDATE");
				found.peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
			}
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
	}
	else {
		webSocket_turnOff();
	}
}

async function createNewRTCPeerConnection(localDescriptionType, remoteDescription, addStreams = false) {
	let pc = new RTCPeerConnection(configuration);

	let object = {peerConnection: pc, user_id: currentTargetPeer, type: "in"};
	if (localDescriptionType == 'answer') object.type = "in";
	else object.type = "out";
	peerConnections.push(object);
	
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
	videoTestElement.srcObject = stream;

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

// Call start() to initiate.
async function start(target, addStreams = false) {
	try {
		// Get local stream, show it in self-view, and add it to be sent.
		currentTargetPeer = target;
		console.log("=====================================");
		console.log(currentTargetPeer);
		console.log("=====================================");
		let pc = await createNewRTCPeerConnection('offer', null, addStreams);
	}
	catch (err) {
		console.error(err);
	}
}

function ONTRACK(event) {
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
}