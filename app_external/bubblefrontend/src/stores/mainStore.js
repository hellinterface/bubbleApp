import { defineStore } from "pinia";

export const useMainStore = defineStore("MainStore", {
    state: () => {
        return {
            currentRightHeaderTitle: "shizz"
        }
    }
})