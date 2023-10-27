<template>
	<div id="app">
		<h1>My Todo App!</h1>
		<counter/>
	</div>
</template>

<script>
import counter from '/components/counter.vue'

export default {
	components: {
		counter
	}
}
</script>

<style lang="css">

*, *::before, *::after {
	box-sizing: border-box;
}

#app {
	max-width: 400px;
	margin: 0 auto;
	line-height: 1.4;
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	color: blue;
}

h1 {
	text-align: center;
}
</style>