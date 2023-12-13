<template>
    <div id="sidebarContent">
		<SidebarLogo></SidebarLogo>
		<SidebarSearch></SidebarSearch>
		<div id="sidebar_main">
			<SidebarCategories></SidebarCategories>
			<SidebarFavorites></SidebarFavorites>
		</div>
		<SidebarBottomCall></SidebarBottomCall>
		<SidebarBottomUser></SidebarBottomUser>
	</div>
</template>

<script>
import SidebarLogo from './SidebarLogo.vue'
import SidebarCategories from './SidebarCategories.vue'
import SidebarSearch from './SidebarSearch.vue'
import SidebarBottomCall from './SidebarBottomCall.vue'
import SidebarBottomUser from './SidebarBottomUser.vue'
import SidebarFavorites from './SidebarFavorites.vue'

export default {
	name: 'SidebarMain',
	components: {
		SidebarLogo,
		SidebarCategories,
		SidebarSearch,
		SidebarBottomCall,
		SidebarBottomUser,
		SidebarFavorites
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#sidebarContent {
	display: flex;
	flex-direction: column;
	width: 100%;
	height: 100%;
	gap: 6px;
}
#sidebar_main {
	display: flex;
	flex-grow: 1;
	flex-direction: column;
}
#sidebarContent > div {
    box-shadow: 0 0 6px #0004;
    border-radius: 6px;
    overflow: hidden;
}
</style>
