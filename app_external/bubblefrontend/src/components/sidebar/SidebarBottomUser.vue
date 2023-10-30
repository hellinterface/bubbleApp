<template>
    <div id="sidebarBottomUser">
        <div id="sidebarBottomUser_avatar"></div>
        <div id="sidebarBottomUser_info">
            <div id="sidebarBottomUser_visiblename"></div>
            <div id="sidebarBottomUser_handle"></div>
        </div>
    </div>
</template>

<script>
export default {
	name: 'SidebarBottomUser'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#sidebarBottomUser {
    background-color: #fff;
    background: linear-gradient(#fff, #eff);
    height: 48px;
    display: flex;
    align-items: center;
    padding: 4px;
}
#sidebarBottomUser_avatar {
    background: plum;
    height: 100%;
    aspect-ratio: 1;
    border-radius: 6px;
}
</style>
