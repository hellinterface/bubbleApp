<template>
    <div id="rightMainHeaderContent">
		<div id="rightMainHeaderContent_title">
			{{currentTitle}}
		</div>
		<div id="rightMainHeaderContent_buttonSetContainer">
			<hbsGrouplist></hbsGrouplist>
		</div>
	</div>
</template>

<script>
import hbsGrouplist from '@/components/headerButtonSets/hbsGrouplist.vue';

export default {
	name: 'RightMainHeader',
	components: {
		hbsGrouplist
	},
	props: {
		//currentButtonSet: {default: hbsContacts},
		currentTitle: {
			type: String,
			default: "Nothing."
		},
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
