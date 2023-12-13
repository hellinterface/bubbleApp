<template>
	<div class="router-view-container" id="rvSettings">
		<div class="secondarySidebar">
			<div class="settings_categories">
				<ChannelLink v-for="category in categoryList" :key="category.id" :channel_title="category.title"></ChannelLink>
			</div>
		</div>
		<div class="routerView_mainContent">
			<AvatarPicker></AvatarPicker>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue'
import { useMainStore } from '@/stores/mainStore'
import ChannelLink from '../elements/ChannelLink.vue'
import AvatarPicker from '../elements/AvatarPicker.vue';
const headerTitle = "Настройки";
var mainStore;

const categoryList = ref([
    {id: "123", title: "Аккаунт"},
    {id: "456", title: "Система"},
]);

export default {
	name: 'RvSettings',
	components: {
		ChannelLink,
		AvatarPicker
	},
	mounted() {
		mainStore = useMainStore();
		mainStore.currentRightHeaderTitle = headerTitle;
		console.log(mainStore.currentRightHeaderTitle);
	},
	data() {
		return {
			categoryList
		}
	}
}
</script>

<style scoped>
	#rvSettings {
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
