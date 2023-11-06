<template>
	<div class="router-view-container" id="rvChats">
		<div class="secondarySidebar">
			<div class="chats_chatList">
				<ChannelLink v-for="channel in groupList" :key="channel.id" :channel_title="channel.title"></ChannelLink>
			</div>
		</div>
		<div class="routerView_mainContent">
			<ChatView></ChatView>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue'
import { useMainStore } from '@/stores/mainStore'
import ChannelLink from '../elements/ChannelLink.vue'
import ChatView from '../ChatView.vue'
const headerTitle = "Диалоги";
var mainStore;

const groupList = ref([
    {id: "123", title: "user1"},
    {id: "456", title: "user2"},
]);

export default {
	name: 'RvChats',
    components: {
        ChannelLink,
		ChatView
    },
	mounted() {
		mainStore = useMainStore();
		mainStore.currentRightHeaderTitle = headerTitle;
		console.log(mainStore.currentRightHeaderTitle);
	},
    data() {
        return {
            groupList
        }
    }
}
</script>

<style scoped>
	#rvChats {
		height: 100%;
		display: flex;
		flex-direction: row;
		gap: 6px;
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
