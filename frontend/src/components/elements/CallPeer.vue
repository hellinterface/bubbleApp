<template>
    <div class="callPeer">
        <div class="callPeer_avatar"></div>
		<video class="callPeer_video" ref="element_video"></video>
        <div class="callPeer_bottom">
            <div class="callPeer_name"></div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

const element_video = ref(null)

	export default {
		name: 'CallPeer',
		props: {
			peerObject: {
				type: Object
			}
		},
		methods: {
			setVideoSourceObject(srcObject) {
				element_video.value.srcObject = srcObject;
			},
		},
		setup() {
			return {
				element_video
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