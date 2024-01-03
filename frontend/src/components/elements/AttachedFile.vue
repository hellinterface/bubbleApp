<template>
	<div class="attachedFile">
        <div class="attachedFile_icon"></div>
        <div class="attachedFile_informationContainer">
            <div class="attachedFile_informationTitle">{{ fileObject.title }}</div>
            <div class="attachedFile_informationSize"> {{ convertSize(fileObject.size) }}</div>
        </div>
        <div class="attachedFile_download">
            <icon>download</icon>
        </div>
	</div>
</template>

<script>

export default {
	name: 'AttachedFile',
	components: {
	},
    props: {
        fileObject: {
            type: Object,
            default: () => {return {id: -1, title: "FILE.EXT", size: 0}}
        }
    },
    methods: {
        convertSize(n) {
            return `${n} байтов`
        }
    },
    setup() {

    },
	mounted() {
	}
}
</script>

<style scoped>
.attachedFile {
    background: #eef;
    border: solid 1px #0004;
    box-shadow: 0 2px 4px #0003;
    border-radius: 6px;
    display: flex;
    flex-direction: row;
    gap: 6px;
    padding: 6px;
    color: #222;
    height: 48px;
}
.attachedFile_icon {
    aspect-ratio: 1;
    background: url(../../assets/images/file_icon.svg);
    max-width: 100%;
    max-height: 100%;
    height: calc(48px - 6px*2);
    filter: drop-shadow(0 2px 3px #0003);
}
.attachedFile_informationContainer {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
}
.attachedFile_download {
    aspect-ratio: 1;
    max-width: 100%;
    max-height: 100%;
    height: calc(48px - 6px*2);
    line-height: calc(48px - 6px*2 + 14px);
    background: #2222;
    text-align: center;
    border-radius: 6px;
}
</style>
