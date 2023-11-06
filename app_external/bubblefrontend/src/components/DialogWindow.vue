<template>
	<div class="dialogWindow">
        <div class="dialogWindowHeader">
            <XButton class="dialogWindowCloseButton" icon_name="close" appearance="outlined"></XButton>
        </div>
        <div class="dialogWindowContent">
            <slot></slot>
        </div>
	</div>
</template>

<script>
import XButton from './elements/XButton.vue';
export default {
	name: 'DialogWindow',
	components: {
        XButton
	},
}
</script>

<style scoped>
.dialogWindow {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    margin: auto;
    width: 400px;
    height: 300px;
    background: white;
    box-shadow: 0 2px 8px #0004;
    display: flex;
    flex-direction: column;
}

.dialogWindowHeader {
    width: 100%;
    display: flex;
    justify-content: flex-end;
}

.dialogWindowCloseButton {
    padding: 3px;
}

.dialogWindowContent {
    flex-grow: 1;
}
</style>
