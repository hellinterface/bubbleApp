<template>
    <div class="fileEntry">
		<div>{{fileObject.title}}</div>
		<div>{{fileObject.size}}</div>
    </div>
</template>

<script>
	export default {
		name: 'FileEntry',
		props: {
			fileObject: {
				type: Object
			}
		},
		setup() {
		}
	}
</script>

<style scoped>
.fileEntry {
    border-bottom: solid 1px #0002;
    min-height: 32px;
    background: #fff;
    padding: 8px 16px;
	display: grid;
	grid-template-columns: 1fr 1fr;
	transition: 0.2s ease;
}
.fileEntry:hover {
	background: #f2f6ff;
}
</style>