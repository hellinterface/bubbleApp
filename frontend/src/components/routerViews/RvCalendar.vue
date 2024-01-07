<template>
    <div class="router-view-container" id="rvCalendar">
        <div class="calendar_buttonsContainer">
            <XButton icon_name="arrow_back" @click="subtractTime()"></XButton>
            <XButton @click="resetTime()">Сейчас</XButton>
            <XButton icon_name="arrow_forward" @click="addTime()"></XButton>
        </div>
        <div class="calendar_week">
            <CalendarDay v-for="day in dayList" :key="day.id" :dayObject="day"></CalendarDay>
        </div>
    </div>
</template>

<script>
import { ref, watch } from 'vue'
import CalendarDay from "../elements/CalendarDay.vue"
import { useMainStore } from '@/stores/mainStore'
import XButton from '../elements/XButton.vue';
import { storeToRefs } from 'pinia';
const headerTitle = "Календарь";
var mainStore;

const dayList = ref([]);
const eventList = ref([

]);
const cursor = ref(0);
export default {
	name: 'RvCalendar',
    components: {
        CalendarDay,
        XButton
    },
    methods: {
        addTime() {
            cursor.value = new Date(cursor.value.getTime()+86400000*7);
            console.log(cursor.value.getDate());
        },
        subtractTime() {
            cursor.value = new Date(cursor.value.getTime()-86400000*7);
            console.log(cursor.value.getDate());
        },
        resetTime() {
            let d = new Date()
            cursor.value = new Date(`${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`);
        }
    },
    setup() {
        function refresh() {
            let now = cursor.value;
            let arr = [];
            let dayOfTheWeek = now.getDay()-1;
            let startPoint = new Date(now.getTime() - dayOfTheWeek * 86400000).getTime();
            if (dayOfTheWeek == -1) dayOfTheWeek = 6;
            for (let i = 0; i < 7; i++) {
                let o = new Date(startPoint + i * 86400000);
                console.log(startPoint + i * 86400000);
                let events = [];
                for (let event of eventList.value) {
                    console.log(event);
                    if (event.date == `${o.getFullYear()}-${o.getMonth()+1}-${o.getDate()}`) {
                        events.push(event);
                    }
                }
                arr.push({date: o, events: events});
            }
            dayList.value = arr;
            console.log(arr);
        }
		mainStore = useMainStore();
        let storeAsRefs = storeToRefs(mainStore);
        let d = new Date();
        cursor.value = new Date(`${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`);
        console.log(cursor.value);
        watch(() => cursor.value, () => {
            refresh();
        });
        watch(() => storeAsRefs.currentUser, () => {
            eventList.value = storeAsRefs.currentUser.value.events;
            console.log("OOOOOOOOOOOOOOOH");
            refresh();
        }, {immediate: true, deep: true})
        return {
            dayList,
            refresh
        }
    },
	mounted() {
		mainStore.header.title = headerTitle;
		console.log(mainStore.header.title);
	},
}
</script>

<style scoped>

#rvCalendar {
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.calendar_month {
    display: grid;
    gap: 3px;
    grid-template-columns: repeat(7, 1fr);
    grid-template-rows: repeat(5, 1fr);
    flex-grow: 1;
}
.calendar_week {
    display: grid;
    gap: 6px;
    grid-template-rows: repeat(7, 1fr);
    flex-grow: 1;
    min-height: 0;
}
.calendar_buttonsContainer {
    display: flex;
    justify-content: center;
    gap: 6px;
}
</style>
