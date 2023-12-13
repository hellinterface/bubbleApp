<template>
	<div class="avatarPicker">
        <div v-for="avatar in avatarList" :key="avatar.id" class="avatarPicker_avatar">
            <img :src="'http://localhost:7070/api/files/get/' + avatar.id" />
        </div>
	</div>
</template>

<script>
import { ref } from 'vue'

const avatarList = ref([
    {id: "permanent_avatar1"},
    {id: "permanent_avatar2"},
    {id: "permanent_avatar3"},
]);

export default {
	name: 'AvatarPicker',
	components: {
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
}
.avatarPicker_avatar img {
    width: 100%;
    height: 100%;
}
</style>
