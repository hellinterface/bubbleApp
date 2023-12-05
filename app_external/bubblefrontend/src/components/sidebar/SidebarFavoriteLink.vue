<template>
    <div class="sidebar_listItem">
        <div class="sidebar_listItem_image"></div>
        <slot></slot>
    </div>
</template>
    
<script>
    export default {
        name: 'SidebarFavoriteLink',
        components: {
        },
        props: {
        }
    }
</script>

<style scoped>

.sidebar_listItem_image {
    background: gray;
    border-radius: 50%;
    width: 28px;
    height: 28px;
}
</style>