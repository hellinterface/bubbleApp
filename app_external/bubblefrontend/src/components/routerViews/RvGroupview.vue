<template>
	<div class="rvGroupview">
		<div class="secondarySidebar">
			<div class="groupView_channelList">
				<ChannelLink v-for="channel in channelList" :key="channel.id" :channel_title="channel.title"></ChannelLink>
			</div>
		</div>
		<div class="routerView_mainContent">
			<CallView></CallView>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue'
import { useMainStore } from '@/stores/mainStore'
import ChannelLink from '../elements/ChannelLink.vue'
import CallView from '../CallView.vue';
const headerTitle = "group1";
var mainStore;

const channelList = ref([
    {id: "123", title: "channel1"},
    {id: "456", title: "channel2"},
]);

export default {
	name: 'RvGroupview',
	components: {
		ChannelLink,
		CallView
	},
	mounted() {
		mainStore = useMainStore();
		mainStore.currentRightHeaderTitle = headerTitle;
		console.log(mainStore.currentRightHeaderTitle);
	},
	data() {
		return {
			channelList
		}
	}
}
</script>

<style scoped>
	.rvGroupview {
		height: 100%;
		display: flex;
		flex-direction: row;
		gap: 6px;
	}
	.secondarySidebar {
		height: 100%;
		width: 20%;
		background-color: #fff;
		box-shadow: 0 0 6px #0004;
		border-radius: 6px;
		padding: 6px;
	}
	.groupView_channelList {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}
	.routerView_mainContent {
		flex-grow: 1;
	}
</style>
