<template>
    <div id="sidebarBottomCall">
        <div id="sidebarBottomCall_currentCallInfo"></div>
        <button>
            <icon>close</icon>
        </button>
        <button>
            <icon>videocam</icon>
        </button>
        <button>
            <icon>mic</icon>
        </button>
        <button>
            <icon>headset_mic</icon>
        </button>
    </div>
</template>

<script>
export default {
	name: 'SidebarBottomCall'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
button {
    padding: 0;
    width: 30px;
    height: 30px;
    background: #0002;
}
button icon {
    font-size: 20px;
    line-height: 28px;
    color: var(--color-primary)
}
</style>
