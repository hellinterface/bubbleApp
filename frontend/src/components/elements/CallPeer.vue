<template>
    <div class="callPeer">
        <div class="callPeer_avatar"></div>
        <div class="callPeer_bottom">
            <div class="callPeer_name"></div>
        </div>
    </div>
</template>

<script>
	export default {
		name: 'CallPeer',
		props: {
			day_number: {
				default: 0,
				type: Number
			},
		}
	}
</script>

<style scoped>
.callPeer {
    border: solid 1px #0002;
    min-width: 64px;
    min-height: 64px;
	border-radius: 6px;
	transition: 0.2s ease;
	padding: 8px;
    background: plum;
}
</style>