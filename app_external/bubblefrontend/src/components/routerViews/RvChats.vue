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
const headerTitle = "Настройки";
var mainStore;

const groupList = ref([
    {id: "123", title: "owo"},
    {id: "456", title: "booyea"},
]);

export default {
	name: 'RvChats',
    components: {
        ChannelLink
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
