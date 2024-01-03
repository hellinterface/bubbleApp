<template>
    <div id="sidebarContent">
		<SidebarLogo></SidebarLogo>
		<!--<SidebarSearch></SidebarSearch>-->
		<div id="sidebar_main">
			<div class="snow"></div>
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
//import SidebarSearch from './SidebarSearch.vue'
import SidebarBottomCall from './SidebarBottomCall.vue'
import SidebarBottomUser from './SidebarBottomUser.vue'
import SidebarFavorites from './SidebarFavorites.vue'

export default {
	name: 'SidebarMain',
	components: {
		SidebarLogo,
		SidebarCategories,
		//SidebarSearch,
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
	position: relative;
}
#sidebarContent > div {
    box-shadow: 0 0 6px #0004;
    border-radius: 6px;
    overflow: hidden;
}

.snow {
	position: absolute;
	width: 100%;
	height: 100%;
	background-image: url("data:image/svg+xml,%3Csvg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' viewBox='0 0 50 50' style='enable-background:new 0 0 50 50%3B' xml:space='preserve'%3E%3Cstyle type='text/css'%3E.st1%7Bopacity:0.3%3Bfill:%23FFFFFF%3B%7D.st3%7Bopacity:0.1%3Bfill:%23FFFFFF%3B%7D%3C/style%3E%3Ccircle class='st1' cx='5' cy='8' r='1'/%3E%3Ccircle class='st1' cx='38' cy='3' r='1'/%3E%3Ccircle class='st1' cx='12' cy='4' r='1'/%3E%3Ccircle class='st1' cx='16' cy='16' r='1'/%3E%3Ccircle class='st1' cx='47' cy='46' r='1'/%3E%3Ccircle class='st1' cx='32' cy='10' r='1'/%3E%3Ccircle class='st1' cx='3' cy='46' r='1'/%3E%3Ccircle class='st1' cx='45' cy='13' r='1'/%3E%3Ccircle class='st1' cx='10' cy='28' r='1'/%3E%3Ccircle class='st1' cx='22' cy='35' r='1'/%3E%3Ccircle class='st1' cx='3' cy='21' r='1'/%3E%3Ccircle class='st1' cx='26' cy='20' r='1'/%3E%3Ccircle class='st1' cx='30' cy='45' r='1'/%3E%3Ccircle class='st1' cx='15' cy='45' r='1'/%3E%3Ccircle class='st1' cx='34' cy='36' r='1'/%3E%3Ccircle class='st1' cx='41' cy='32' r='1'/%3E%3C/svg%3E");
	background-position: 0px 0px;
	background-size: 100px;
	background-repeat: repeat;
	animation: snowBG 10s linear infinite;
	filter: invert(1) blur(1px);
	opacity: 0.25;
}

@keyframes snowBG {
  0% {
	background-position: 0 0;
  }
  100% {
	background-position: 0px 100px;
  }
}
</style>
