<template>
	<div id="sidebar">
		<SidebarMain></SidebarMain>
	</div>  
	<div id="rightSide"></div>
</template>

<script>
import SidebarMain from '../components/Sidebar.vue'

export default {
	name: 'App',
	components: {
		SidebarMain
	}
}
</script>

<style>
#sidebar {
    height: 100%;
    width: 15vw;
    min-width: 220px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    z-index: 20;
    flex-shrink: 0;
    gap: 6px;
}
#rightSide {
    flex-grow: 1;
    border-radius: 6px;
    z-index: 18;
}
</style>
