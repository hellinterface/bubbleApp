<template>
	<div class="groupList_card" @click.right.prevent="(event) => {mainStore.contextMenu.show(event, contextMenuObject)}">
		<div class="groupList_avatar"></div>
		<div class="groupList_title">{{ group_title }}</div>
		<XButton class="groupList_moreMenuButton" icon_name="more_vert" appearance="round small"></XButton>
	</div>
</template>

<script>
    import { useMainStore } from '@/stores/mainStore'
    import XButton from './XButton.vue';
	export default {
		name: 'GroupCard',
        components: {
            XButton
        },
		props: {
			group_title: {
				default: "GROUPTITLE",
				type: String
			},
		},
        setup() {
			const mainStore = useMainStore();
			return {
				mainStore
			}
        },
		data() {
            return {
                contextMenuObject: [
                    {text: "View group", onclick: () => {console.log("VIEW GROUP")}},
                    {text: "Edit group", onclick: () => {console.log("EDIT GROUP")}},
                    {text: "Leave group", onclick: () => {console.log("LEAVE GROUP")}},
                ]
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
    flex-basis: 400px;
    height: 200px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: 0.2s ease;
    position: relative;
    flex-shrink: 1;
    flex-grow: 1;
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
}

.groupList_title {
    font-weight: bold;
    font-size: 24px;
}
</style>