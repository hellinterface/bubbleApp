<template>
    <BBRouterLink v-bind="$props">
        <div class="bottombar_listItem">
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
	name: 'BottombarCategoryLink',
    components: {
        BBRouterLink
    },
    props: {
        icon_name: String,
        ...BBRouterLink.props
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bottombar_listItem {
    position: relative;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 16px;
    font-weight: 500;
    transition: 0.4s ease;
    gap: 8px;
    font-size: 0.75em;
}

a {
    text-decoration: none;
    color: unset;
}


.bottombar_listItem::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 6px;
    width: calc(100% - 6px*2);
    height: 1px;
    background: #0002;
}

.bottombar_listItem::before {
    content: "";
    position: absolute;
    top: 6px;
    left: 6px;
    width: calc(100% - 6px*2);
    height: calc(100% - 6px*2);
    opacity: 0;
    background: linear-gradient(transparent, var(--color-primary));
    border-radius: 4px;
    transition: 0.2s ease;
}

.bottombar_listItem:hover::before  {
    opacity: 0.5;
}

.bottombar_listItem:hover {
    cursor: pointer;
}
</style>
