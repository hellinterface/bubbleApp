<template>
	<div class="dialogWindow" ref="ROOT">
        <div class="dialogWindowHeader">
            <XButton class="dialogWindowCloseButton" icon_name="close" appearance="outlined" @click="close()"></XButton>
        </div>
        <div class="dialogWindowContent" ref="contentContainer">
            <slot></slot>
        </div>
	</div>
</template>

<script>
import { ref, createApp, toRefs } from 'vue';
import XButton from './elements/XButton.vue';
const contentContainer = ref(null);
var fragment;
var fragmentInstance;
const ROOT = ref(null);
export default {
	name: 'DialogWindow',
	components: {
        XButton
	},
    props: {
		fragment: {
			type: Object
		}
    },
    methods: {
        close() {
            console.log("CLOSING DIALOG WINDOW");
            ROOT.value.remove();
        }
    },
    setup(props) {
        fragment = toRefs(props).fragment;
        console.log("SETTING FRAGMENT");
        console.log(fragment.value);
        fragmentInstance = createApp(fragment.value);
        return {
            contentContainer,
            ROOT
        }
    },
    mounted() {
        let fragmentWrapper = document.createElement('div');
        fragmentWrapper.classList.add('fragmentWrapper');
        contentContainer.value.appendChild(fragmentWrapper);
        fragmentInstance.mount(fragmentWrapper);
    },
    created() {
    }
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

.fragmentWrapper {
    height: 100%;
}
</style>
