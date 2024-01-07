<template>
	<div class="groupList_card" :style="{ background: `linear-gradient(145deg, white, ${group_object.color}33)` }" @click.right.prevent="(event) => {mainStore.contextMenu.show(event, contextMenuObject)}">
		<div class="groupList_avatar" :style="{ backgroundColor: group_object.color }"></div>
		<div class="groupList_title">{{ group_object.title }}</div>
	</div>
</template>

<script>
    import { useMainStore } from '@/stores/mainStore'
    import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
	export default {
		name: 'GroupCard',
        components: {
        },
		props: {
			group_object: {
				type: Object
			},
		},
        methods: {
        },
        setup(props) {
			const mainStore = useMainStore();
            const router = useRouter()
            var openGroup = function() {
                router.push("/groupview/"+props.group_object.id)
            };
            var contextMenuObject = ref([
                {text: "Открыть группу", onclick: () => {openGroup()}}
            ]);
            console.log(props.group_object.owner.id, mainStore.currentUser.id);
            if (props.group_object.owner.id == mainStore.currentUser.id) {
                console.log("SETINGS");
                contextMenuObject.value.push({text: "Настройки группы", onclick: () => {console.log("EDIT GROUP")}});
            }
            else {
                console.log("LEAVE");
                contextMenuObject.value.push({text: "Покинуть группу", onclick: () => {console.log("LEAVE GROUP")}});
            }
            onMounted(() => {
            });
			return {
				mainStore,
                contextMenuObject,
                openGroup
			}
        },
		data() {
		}
	}
</script>

<style scoped>
.groupList_card {
    background: #fdfdfd;
    border: solid 1px #0243;
    border-radius: 4px;
    box-shadow: 0 4px 4px #0002;
    flex-basis: 400px;
    height: 200px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: 0.2s ease;
    position: relative;
    flex-shrink: 1;
    flex-grow: 1;
}

.groupList_card:hover {
    background: #fff;
    box-shadow: 0 8px 12px #0002;
}

.groupList_moreMenuButton {
    width: 32px;
    height: 32px;
    position: absolute;
    right: 16px;
    top: 16px;
}

.groupList_avatar {
    width: 80px;
    height: 80px;
    background: slateblue;
    border-radius: 4px;
    box-shadow: 0 2px 2px #0004;
}

.groupList_title {
    font-weight: bold;
    font-size: 24px;
}
</style>