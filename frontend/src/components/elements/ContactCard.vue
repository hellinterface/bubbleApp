<template>
	<div class="groupList_card" @click.right.prevent="(event) => {mainStore.contextMenu.show(event, contextMenuObject)}">
		<div class="groupList_avatar"></div>
		<div class="groupList_title">{{ contact_object.visible_name }}</div>
		<XButton class="groupList_moreMenuButton" icon_name="more_vert" appearance="round small"></XButton>
        <div class="groupList_actions">
            <XButton icon_name="call" appearance="outlined"></XButton>
            <XButton icon_name="chat" appearance="outlined" @click="openChatWithUser(contact_object.id)"></XButton>
        </div>
	</div>
</template>

<script>
    import { useMainStore } from '@/stores/mainStore'
    //import axios from 'axios';
    import XButton from './XButton.vue';
	var mainStore;

	export default {
		name: 'ContactCard',
        components: {
            XButton
        },
		props: {
			contact_object: {
				type: Object
			},
		},
        methods: {
            openChatWithUser(user_id) {
                this.$router.push("/chats/"+user_id);
                /*
                axios.get(location.protocol+`//127.0.0.1:7070/api/messaging/getPersonalChatBetweenUsers/?user1='${mainStore.currentUser.id}&user2=${user_id})`, {withCredentials: true})
                .then(res => {
                    console.log(res);
                })
                .catch(err => {
                    console.log(err);
                        axios.post(location.protocol+`//127.0.0.1:7070/api/messaging/createConversation/?user1='${mainStore.currentUser.id}&user2=${user_id})`, {withCredentials: true})
                        .then(res => {
                            console.log(res);
                        })
                        .catch(err => {
                            console.log(err);
                        })
                })*/
            }
        },
        setup() {
            mainStore = useMainStore();
			return {
				mainStore
			}
        },
		data() {
            return {
                contextMenuObject: [
                    {text: "Call", onclick: () => {console.log("CALL")}},
                    {text: "Chat", onclick: () => {console.log("CALL")}},
                    {text: "Edit contact", onclick: () => {console.log("EDIT CONTACT")}},
                    {text: "Remove contact", onclick: () => {console.log("REMOVE CONTACT")}},
                ]
            }
		}
	}
</script>

<style scoped>
.groupList_card {
    background: #fdfdfd;
    border: solid 1px #0243;
    border-radius: 4px;
    box-shadow: 0 4px 4px #0002;
    flex-basis: 300px;
    min-height: 180px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: 0.2s ease;
    position: relative;
    flex-shrink: 1;
    flex-grow: 1;
    align-items: center;
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
    flex-shrink: 0;
}

.groupList_title {
    font-weight: bold;
    font-size: 24px;
}

.groupList_actions {
    display: flex;
    gap: 6px;
}
</style>