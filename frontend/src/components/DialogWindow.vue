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
var fragmentProps;
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
		},
        fragmentProps: {
            type: Object,
            default: () => {}
        }
    },
    methods: {
        close() {
            console.log("CLOSING DIALOG WINDOW");
            fragmentInstance.unmount();
            ROOT.value.remove();
        }
    },
    setup(props) {
        fragment = toRefs(props).fragment;
        fragmentProps = toRefs(props).fragmentProps;
        console.log("SETTING FRAGMENT");
        console.log(fragment.value);
        fragmentInstance = createApp(fragment.value, fragmentProps.value);
        return {
            contentContainer,
            ROOT
        }
    },
    mounted() {
        let fragmentWrapper = document.createElement('div');
        fragmentWrapper.classList.add('fragmentWrapper');
        fragmentWrapper.style = "height: fit-content; width: fit-content; min-width: 100%;"
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
    min-width: 400px;
    background: white;
    box-shadow: 0 4px 12px #0006;
    display: flex;
    flex-direction: column;
    width: fit-content;
    height: fit-content;
    border-radius: 6px;
}

.dialogWindowHeader {
    width: 100%;
    display: flex;
    justify-content: flex-end;
    padding: 8px;
}

.dialogWindowCloseButton {
    padding: 3px;
}

.dialogWindowContent {
    flex-grow: 1;
    height: fit-content;
    width: fit-content;
    min-width: 100%;
    padding: 8px;
    padding-top: 0;
}
</style>
