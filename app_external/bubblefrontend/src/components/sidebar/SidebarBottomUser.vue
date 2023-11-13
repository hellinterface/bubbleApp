<template>
    <div id="sidebarBottomUser">
        <div id="sidebarBottomUser_avatar"></div>
        <div id="sidebarBottomUser_info">
            <div id="sidebarBottomUser_visiblename">{{currentUser.visible_name}}</div>
            <div id="sidebarBottomUser_handle">@{{currentUser.handle}}</div>
        </div>
        <button @click="console.log(currentUser)"></button>
        <BBRouterLink to="/settings">
            <XButton id="sidebarBottomUser_settingsButton" icon_name="settings" appearance="small"></XButton>
        </BBRouterLink>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useMainStore } from '@/stores/mainStore';
import XButton from '../elements/XButton.vue';
import BBRouterLink from '../BBRouterLink.vue';
export default {
	name: 'SidebarBottomUser',
    components: {
        XButton,
        BBRouterLink
    },
	setup() {
		const mainStore = useMainStore();
        const currentUser = ref(mainStore.currentUser);
        mainStore.$subscribe((mutation, state) => {
            console.warn("STATE");
            console.log(state);
            //currentUser.value = state
        });
		return {
			currentUser
		}
	}
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
    gap: 4px;
}
#sidebarBottomUser_avatar {
    background: plum;
    height: 100%;
    aspect-ratio: 1;
    border-radius: 6px;
}
#sidebarBottomUser_info {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
}
#sidebarBottomUser_visiblename {
    font-weight: bold;
}
#sidebarBottomUser_handle {
    color: #000c;
    font-size: 0.8em;
}
#sidebarBottomUser_settingsButton {
    height: 32px;
    width: 32px;
}
a {
    color: unset;
    text-decoration: none;
}
</style>
