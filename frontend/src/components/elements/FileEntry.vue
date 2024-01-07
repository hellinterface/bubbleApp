<template>
    <div class="fileEntry">
		<div>{{fileObject.title}}</div>
		<div>{{sizeConvert(fileObject.size)}}</div>
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
		setup(props) {
			console.log(props.fileObject);
			
		},
		methods: {
			sizeConvert(bytes) {
				let units = [' Б', ' КБ', ' МБ', ' ГБ'];
				let unit_int = 0;
				let temp_big   = bytes;
				let temp_small = (bytes / 1024);
				while (temp_small > 1) {
					unit_int++;
					temp_big = temp_small;
					temp_small = (temp_small / 1024)
				}
				return (Math.round(temp_big * 100) / 100) + units[unit_int]
			}
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