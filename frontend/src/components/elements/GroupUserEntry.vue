<template>
	<div class="groupUserEntry">
		<div class="groupUserEntry_avatar" ref="element_avatar" :style="{backgroundImage: `url('${win_location.protocol}//${win_location.hostname}:7070/api/files/download/${user_object.avatar_fileid}')`}"></div>
		<div class="groupUserEntry_visibleName">{{ user_object.visible_name }}</div>
	</div>
</template>

<script>
    import { useMainStore } from '@/stores/mainStore'
	//import axios from 'axios';
	import { ref } from 'vue';
	//const element_avatar = ref(null);
	var win_location = ref(window.location);
	
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
				mainStore,
				win_location
			}
        },
		mounted() {
			/*
			axios.get(location.protocol+"//"+location.hostname+":7070/api/files/download/"+this.user_object.avatar_fileid)
			.then(res => {
				console.log(res);
				element_avatar.style.backgroundImage = `url(${res})`
			})
			.catch(err => {
				console.log(err);
			})
			*/
		},
		data() {
		}
	}
</script>

<style scoped>
.groupUserEntry {
	display: flex;
	flex-direction: row;
	gap: 6px;
	align-items: center;
}

.groupUserEntry_avatar {
	background: plum;
	width: 36px;
	height: 36px;
	border-radius: 50%;
	box-shadow: 0 2px 4px #0004;
}
</style>