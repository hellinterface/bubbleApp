<template>
	<div class="avatarPicker">
        <div v-for="avatar in avatarList" :key="avatar.id" class="avatarPicker_avatar">
            <img :src="'http://localhost:7070/api/files/download/' + avatar.id" />
        </div>
	</div>
</template>

<script>
import { ref } from 'vue'

const avatarList = ref([
    {id: 1},
    {id: 2},
    {id: 3},
    {id: 4},
    {id: 5},
    {id: 6},
]);

export default {
	name: 'AvatarPicker',
	components: {
	},
    setup() {
        
    },
	mounted() {
	},
	data() {
		return {
            avatarList
		}
	}
}
</script>

<style scoped>
.avatarPicker {
    display: flex;
    gap: 6px;
}
.avatarPicker_avatar {
    border-radius: 50%;
    box-shadow: 0 2px 4px #0004;
    width: 100px;
    height: 100px;
    overflow: hidden;
    flex-shrink: 0;
}
.avatarPicker_avatar img {
    width: 100%;
    height: 100%;
}
</style>
