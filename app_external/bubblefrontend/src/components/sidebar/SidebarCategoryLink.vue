<template>
    <BBRouterLink v-bind="$props">
        <div class="sidebar_listItem">
            <icon>{{icon_name}}</icon>
            <div>
                <slot></slot>
            </div>
        </div>
    </BBRouterLink>
</template>
    
<script>
    import BBRouterLink from '../BBRouterLink.vue';
    
    export default {
        name: 'SidebarCategoryLink',
        components: {
            BBRouterLink
        },
        props: {
            icon_name: String,
            ...BBRouterLink.props
        }
    }
</script>

<style scoped>
    #sidebarCategory_mainLinks {
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

    a {
        text-decoration: none;
        color: unset;
    }
    
    #sidebarCategory_favorites .sidebar_listItem {
        height: 42px;
        padding: 8px;
        gap: 8px;
    }
    
    #sidebarCategory_favorites .sidebar_listItem:hover {
        background: #0002;
    }
    
    #sidebarCategory_mainLinks .sidebar_listItem::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 6px;
        width: calc(100% - 6px*2);
        height: 1px;
        background: #0002;
    }
    
    #sidebarCategory_mainLinks .sidebar_listItem::before {
        content: "";
        position: absolute;
        top: 6px;
        left: 6px;
        width: calc(100% - 6px*2);
        height: calc(100% - 6px*2);
        opacity: 0;
        background: linear-gradient(30deg, var(--color-primary), transparent);
        border-radius: 4px;
        transition: 0.2s ease;
    }
    
    #sidebarCategory_mainLinks .sidebar_listItem:hover::before  {
        opacity: 0.5;
    }
    
    #sidebarCategory_mainLinks .sidebar_listItem:hover {
        padding-left: 30px;
        cursor: pointer;
    }
</style>