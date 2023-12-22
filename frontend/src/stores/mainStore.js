import { defineStore } from "pinia";

export const useMainStore = defineStore("MainStore", {
    state: () => {
        return {
            header: {},
            contextMenu: {},
            currentUser: {}
        }
    }
})