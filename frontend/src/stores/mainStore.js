import { defineStore } from "pinia";

export const useMainStore = defineStore("MainStore", {
    state: () => {
        return {
            currentChannelId: -1,
            currentFolderId: -1,
            header: {},
            contextMenu: {},
            currentUser: {},
            root: {
            },
            rtc: {
                peerList: [],
                callPeerYou: null
            },
        }
    }
})