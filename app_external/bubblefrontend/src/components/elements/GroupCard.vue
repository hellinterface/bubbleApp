<template>
	<div class="groupList_card">
		<div class="groupList_avatar"></div>
		<div class="groupList_title">{{ group_title }}</div>
		<div class="groupList_moreMenuButton">
			<icon>more_vert</icon>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'GroupCard',

		props: {
			group_title: {
				default: "GROUPTITLE",
				type: String
			},
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
    border-radius: 50%;
    position: absolute;
    right: 16px;
    top: 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: 0.2s ease;
}

.groupList_moreMenuButton:hover {
    background: #0001;
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