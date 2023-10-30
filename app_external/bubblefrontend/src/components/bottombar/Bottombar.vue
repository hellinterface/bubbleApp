<template>
    <div id="bottombarContent">
	</div>
</template>

<script>

export default {
	name: 'BottombarMain',
	components: {
	},
	props: {
		msg: String
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
	#bottombarContent {
		background-color: #fff;
		background: linear-gradient(#eff, #cef);
		width: 100%;
		height: 100%;
		border-radius: 4px;
		box-shadow: 0 4px 12px #0006;
	}
</style>
