<template>
    <div id="sidebarBottomCall">
        <div id="sidebarBottomCall_currentCallInfo">
            <BBRouterLink to="/call">
                Текущее собрание
            </BBRouterLink>
        </div>
        <XButton icon_name="close" appearance="small"></XButton>
        <XButton icon_name="videocam" appearance="small"></XButton>
        <XButton icon_name="mic" appearance="small"></XButton>
        <XButton icon_name="headset_mic" appearance="small"></XButton>
    </div>
</template>

<script>
import BBRouterLink from '../BBRouterLink.vue';
import XButton from '../elements/XButton.vue';

export default {
	name: 'SidebarBottomCall',
    components: {
        XButton,
        BBRouterLink
    }
}
</script>

<style scoped>
#sidebarBottomCall {
    background-color: #fff;
    background: linear-gradient(#fff, #eff);
    height: 48px;
    display: flex;
    align-items: center;
    padding: 4px;
    gap: 3px;
}
</style>
