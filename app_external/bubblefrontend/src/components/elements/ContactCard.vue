<template>
	<div class="groupList_card" @click.right.prevent="mainStore.contextMenu.show()">
		<div class="groupList_avatar"></div>
		<div class="groupList_title">{{ group_title }}</div>
		<XButton class="groupList_moreMenuButton" icon_name="more_vert" appearance="round small"></XButton>
        <div class="groupList_actions">
            <XButton icon_name="call" appearance="outlined"></XButton>
            <XButton icon_name="chat" appearance="outlined"></XButton>
        </div>
	</div>
</template>

<script>
    import { useMainStore } from '@/stores/mainStore'
    import XButton from './XButton.vue';
	export default {
		name: 'ContactCard',
        components: {
            XButton
        },
		props: {
			group_title: {
				default: "GROUPTITLE",
				type: String
			},
		},
		data() {
			const mainStore = useMainStore();
			return {
				mainStore
			}
		}
	}
</script>

<style scoped>
.groupList_card {
    background: #fdfdfd;
    border: solid 1px #0243;
    border-radius: 4px;
    box-shadow: 0 4px 4px #0002;
    flex-basis: 300px;
    min-height: 180px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: 0.2s ease;
    position: relative;
    flex-shrink: 1;
    flex-grow: 1;
    align-items: center;
}

.groupList_card:hover {
    background: #fff;
    box-shadow: 0 8px 12px #0002;
}

.groupList_moreMenuButton {
    width: 32px;
    height: 32px;
    position: absolute;
    right: 16px;
    top: 16px;
}

.groupList_avatar {
    width: 80px;
    height: 80px;
    background: slateblue;
    border-radius: 4px;
    box-shadow: 0 2px 2px #0004;
    flex-shrink: 0;
}

.groupList_title {
    font-weight: bold;
    font-size: 24px;
}

.groupList_actions {
    display: flex;
    gap: 6px;
}
</style>