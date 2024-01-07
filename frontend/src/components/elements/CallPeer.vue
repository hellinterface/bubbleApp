<template>
    <div class="callPeer">
        <div class="callPeer_avatar"></div>
		<video class="callPeer_video" ref="element_video" autoplay></video>
        <div class="callPeer_bottom">
            <div class="callPeer_name"></div>
        </div>
    </div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore';
import { storeToRefs } from 'pinia';
import { onMounted, ref, watch } from 'vue';

var mainStore;

	export default {
		name: 'CallPeer',
		props: {
			peerObject: {
				type: Object
			}
		},
		methods: {
		},
		setup(props) {
			mainStore = useMainStore();
			let storeAsRefs =storeToRefs(mainStore);
			const element_video = ref(null)
			function setVideoSourceObject(srcObject) {
				console.log("%c qwer SETTING VIDEO SOURCE OBJECT", "color: green;");
				console.log(srcObject);
				element_video.value.srcObject = srcObject;
			}
			watch(() => storeAsRefs.rtc.value.peerList.srcObject, (newValue, oldValue) => {
				console.log(newValue, oldValue);
				setVideoSourceObject(props.peerObject.srcObject);
			});
			onMounted(() => {
				element_video.value.onloadedmetadata = function() {
					console.log("LOADED VIDEO METADATA")
				};
				console.log(props.peerObject);
				setVideoSourceObject(props.peerObject.srcObject);
			});
			return {
				element_video,
				setVideoSourceObject
			}
		}
	}
</script>

<style scoped>
.callPeer {
    border: solid 1px #0002;
    min-width: 64px;
    min-height: 64px;
	border-radius: 6px;
	transition: 0.2s ease;
	padding: 8px;
    background: plum;
}
</style>