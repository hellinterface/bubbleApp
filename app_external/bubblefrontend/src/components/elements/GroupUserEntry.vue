<template>
	<div class="groupUserEntry">
		<div class="groupUserEntry_avatar"></div>
		<div class="groupUserEntry_visibleName">{{ user_object.visible_name }}</div>
	</div>
</template>

<script>
    import { useMainStore } from '@/stores/mainStore'
	export default {
		name: 'GroupUserEntry',
        components: {
        },
		props: {
			user_object: {
				type: Object
			},
		},
        setup() {
			const mainStore = useMainStore();
			return {
				mainStore
			}
        },
		data() {
		}
	}
</script>

<style scoped>

</style>