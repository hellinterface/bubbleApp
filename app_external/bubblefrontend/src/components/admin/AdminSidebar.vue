<template>
    <div id="sidebarContent">
		<div id="adminsidebar_logo">BUBBLE ADMIN</div>
		<SidebarSearch></SidebarSearch>
		<div id="sidebar_main">
			<SidebarCategoryLink icon_name="contacts" to="/users">Пользователи</SidebarCategoryLink>
		</div>
		<SidebarBottomUser></SidebarBottomUser>
	</div>
</template>

<script>
import SidebarCategoryLink from '../sidebar/SidebarCategoryLink.vue'
import SidebarSearch from '../sidebar/SidebarSearch.vue'
import SidebarBottomUser from '../sidebar/SidebarBottomUser.vue'

export default {
	name: 'AdminSidebar',
	components: {
		SidebarCategoryLink,
		SidebarSearch,
		SidebarBottomUser
	},
	props: {
		msg: String
	}
}
</script>

<style scoped>
#adminsidebar_logo {
	background: #234;
	color: #eef;
	font-weight: bold;
	font-size: 1.25em;
	display: flex;
	justify-content: center;
	align-items: center;
	height: 80px;
}
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
	background: #fff;
	flex-direction: column;
}
#sidebarContent > div {
    box-shadow: 0 0 6px #0004;
    border-radius: 6px;
    overflow: hidden;
}
</style>
