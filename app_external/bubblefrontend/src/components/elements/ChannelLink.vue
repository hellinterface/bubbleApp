<template>
	<div class="channelLink">
		<div class="channelLink_title">{{ channel_title }}</div>
	</div>
</template>

<script>
	export default {
		name: 'ChannelLink',

		props: {
			channel_title: {
				default: "CHANNELLINK",
				type: String
			},
		}
	}
</script>

<style scoped>
.channelLink {
    border-radius: 6px;
    padding: 4px 8px;
    height: 30px;
    display: flex;
    flex-direction: row;
    align-items: center;
    transition: 0.2s ease;
}
.channelLink:hover {
    background-color: #69a4;
}
</style>