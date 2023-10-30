<template>
    <div id="rightMainHeaderContent">
		<div id="rightMainHeaderContent_title">
			{{currentTitle}}
		</div>
	</div>
</template>

<script>

export default {
	name: 'RightMainHeader',
	components: {
	},
	props: {
		currentTitle: {
			type: String,
			default: "Nothing."
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
	padding: 8px;
	flex-shrink: 0;
}
#rightMainHeaderContent_title {
	font-weight: bold;
	font-size: 1.8em;
}
</style>
