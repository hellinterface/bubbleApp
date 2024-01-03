<template>
    <div id="rightMainHeaderContent">
		<div id="rightMainHeaderContent_title">
			{{currentTitle}}
		</div>
		<div id="rightMainHeaderContent_buttonSetContainer" ref="buttonSetContainer">
		</div>
	</div>
</template>

<script>
import { ref, createApp } from 'vue';
const buttonSetContainer = ref(null);
var fragmentInstance;

export default {
	name: 'RightMainHeader',
	components: {
		//hbsGrouplist
	},
	props: {
		//currentButtonSet: {default: hbsContacts},
		currentTitle: {
			type: String,
			default: "Nothing."
		},
		buttonSet: {
			type: Object
		}
	},
	watch: {
		buttonSet: function (newVal, oldVal) {
			console.warn("--- WATCH UPDATED ---");
			console.log(newVal, oldVal);
            if (fragmentInstance) fragmentInstance.unmount();
			this.setButtonSet(newVal);
		}
	},
	methods: {
		setButtonSet(buttonSetFragment)	{
			console.warn("--- SETTING BUTTON SET ---");
			console.warn(buttonSetFragment);
			let _props = {};
			let propsObject = {
				fragmentProps: _props
			}
			console.log(propsObject);
			fragmentInstance = createApp(buttonSetFragment, propsObject);
			console.log(fragmentInstance);
			console.log(buttonSetContainer.value);
			fragmentInstance.mount(buttonSetContainer.value);
		}
	},
	setup() {
		return {
			buttonSetContainer
		}
	},
	data() {
		return {

		}
	}
}
</script>

<style scoped>
#rightMainHeaderContent {
	height: 80px;
	background: #fff;
	box-shadow: 0 0 6px #0004;
	border-radius: 6px;
	border: solid 1px #0003;
	display: flex;
	align-items: center;
	padding: 8px 24px;
	flex-shrink: 0;
	justify-content: space-between;
}
#rightMainHeaderContent_title {
	font-weight: bold;
	font-size: 1.8em;
}
</style>
