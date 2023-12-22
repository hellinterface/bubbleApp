<template>
    <div class="router-view-container" id="rvCalendar">
        <div class="calendar_month">
            <CalendarDay v-for="day in dayList" :key="day.id" :day_number="day.day"></CalendarDay>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
import CalendarDay from "../elements/CalendarDay.vue"
import { useMainStore } from '@/stores/mainStore'
const headerTitle = "Календарь";
var mainStore;

const dayList = ref([
    {id: "1", day: 1},
    {id: "1", day: 2},
    {id: "1", day: 3},
    {id: "1", day: 4},
    {id: "1", day: 5},
    {id: "1", day: 6},
    {id: "1", day: 7},
    {id: "1", day: 8},
    {id: "1", day: 9},
    {id: "1", day: 10},
    {id: "1", day: 11},
    {id: "1", day: 12},
    {id: "1", day: 13},
    {id: "1", day: 14},
    {id: "1", day: 15},
    {id: "1", day: 16},
    {id: "1", day: 17},
    {id: "1", day: 18},
    {id: "1", day: 19},
    {id: "1", day: 20},
    {id: "1", day: 21},
    {id: "1", day: 22},
    {id: "1", day: 23},
    {id: "1", day: 24},
    {id: "1", day: 25},
    {id: "1", day: 26},
    {id: "1", day: 27},
    {id: "1", day: 28},
    {id: "1", day: 29},
    {id: "1", day: 30},
]);

export default {
	name: 'RvCalendar',
    components: {
        CalendarDay
    },
	mounted() {
		mainStore = useMainStore();
		mainStore.header.title = headerTitle;
		console.log(mainStore.header.title);
	},
    data() {
        return {
            dayList
        }
    }
}
</script>

<style scoped>
.calendar_month {
    display: grid;
    gap: 6px;
    grid-template-columns: repeat(7, 1fr);
}
</style>
