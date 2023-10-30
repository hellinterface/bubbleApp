<template>
    <div id="sidebarCategory_searchContainer">
        <icon id="sidebar_searchIcon">search</icon>
        <input type="text" id="sidebar_searchInput" placeholder="Search">
    </div>
</template>

<script>
export default {
	name: 'SidebarSearch'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#sidebarCategory_searchContainer {
    height: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #fff;
}

#sidebar_searchIcon {
    color: #888;
    margin-left: 16px;
    margin-right: 0px;
}

#sidebar_searchInput {
    background: none;
    border: none;
    flex-grow: 1;
}
</style>
