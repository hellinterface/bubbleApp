<template>
	<div class="callView">
        <div class="callView_main">
            <div class="callView_peerList">
                <CallPeer v-for="peer in peerList" :key="peer.id" :message_object="peer"></CallPeer>
            </div>
        </div>
        <div class="callView_bottomBar stdSurface">
            <XButton icon_name="call_end">Выйти из звонка</XButton>
        </div>
	</div>
</template>

<script>
import { ref } from 'vue'
import CallPeer from './elements/CallPeer.vue'
import XButton from './elements/XButton.vue';

const peerList = ref([
    {id: "123", handle: "owo", visible_name: "owoman"},
    {id: "456", handle: "uwu", visible_name: "uwuman"},
]);

export default {
	name: 'CallView',
	components: {
        CallPeer,
        XButton
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
</style>
