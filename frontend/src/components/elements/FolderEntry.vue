<template>
    <div class="folderEntry">
		<icon>folder</icon>
        {{folderObject.title}}
    </div>
</template>

<script>
	export default {
		name: 'FolderEntry',
		props: {
			folderObject: {
				type: Object
			}
		},
		setup() {
		}
	}
</script>

<style scoped>
.folderEntry {
    border: solid 1px #0002;
    background: #fff;
    padding: 8px 16px;
	border-radius: 6px;
	box-shadow: 0 2px 4px #0004;
	aspect-ratio: 1;
	max-width: 140px;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	gap: 6px;
	transition: 0.2s ease;
}
.folderEntry:hover {
	box-shadow: 0 6px 10px #0003;
}
</style>