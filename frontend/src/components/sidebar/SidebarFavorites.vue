<template>            
<div id="sidebarCategory_mainLinks">
    <SidebarFavoriteLink>Контакт 1</SidebarFavoriteLink>
    <SidebarFavoriteLink>Контакт 2</SidebarFavoriteLink>
    <SidebarFavoriteLink>Контакт 3</SidebarFavoriteLink>
</div>
</template>

<script>
import SidebarFavoriteLink from './SidebarFavoriteLink.vue';

export default {
	name: 'SidebarFavorites',
	components: {
        SidebarFavoriteLink
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#sidebarCategory_favorites {
    display: flex;
    flex-direction: column;
    width: 100%;
    background: #fff;
}

.sidebar_listItem {
    width: 100%;
    position: relative;
    height: 42px;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 12px 16px;
    font-weight: 500;
    transition: 0.4s ease;
    gap: 8px;
    font-size: 1em;
}

#sidebarCategory_favorites .sidebar_listItem {
    height: 42px;
    padding: 8px;
    gap: 8px;
}

#sidebarCategory_favorites .sidebar_listItem:hover {
    background: #0002;
}

</style>