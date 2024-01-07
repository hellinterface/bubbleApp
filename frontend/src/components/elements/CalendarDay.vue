<template>
	<div class="calendarDay">
		<div class="calendarDayTop">
			<div class="calendarDayNumber">{{ topLeftString }}</div>
			<XButton icon_name="add" appearance="small" @click="createEvent(dayObject.date)"></XButton>
		</div>
		<div class="calendarDayEventList">
			<div v-for="event in dayObject.events" :key="event.text" class="calendarDayEventItem">
				<XButton icon_name="delete" appearance="small" @click="deleteEvent(event)"></XButton>
				<textarea :value="event.text" @blur="(e) => onBlur(event, e.target.value)"></textarea>
			</div>
		</div>
	</div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore';
import axios from 'axios';
import { storeToRefs } from 'pinia';
import { ref, watch } from 'vue';
import XButton from './XButton.vue';

var mainStore;

	export default {
		name: 'CalendarDay',
		components: {
			XButton
		},
		props: {
			dayObject: {
				type: Object
			},
		},
		methods: {
			createEvent(d) {
				let event = {date: `${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`, text: ""};
				mainStore.currentUser.events.push(event);
				console.log("CREATED EVENT", event);
				this.saveChanges();
			},
			deleteEvent(event) {
				let index = mainStore.currentUser.events.findIndex(i => i == event);
				mainStore.currentUser.events.splice(index, 1);
				this.saveChanges();
			},
			onBlur(object, value) {
				console.log("ONBLUR");
				object.text = value;
				this.saveChanges();
			},
			saveChanges() {				
				axios.post(location.protocol+"//"+location.hostname+":7070/api/users/update",
					{events: mainStore.currentUser.events},
					{withCredentials: true})
				.then(res => {
					console.log(res);
				})
				.catch(err => {
					console.log(err);
				})
			}
		},
		setup(props) {
			mainStore = useMainStore();
			let storeAsRefs = storeToRefs(mainStore);
			console.log(storeAsRefs);
			const topLeftString = ref('-');
			watch(() => props.dayObject, () => {
				console.log(mainStore.currentUser.events);
				let date = props.dayObject.date;
				topLeftString.value = date.getDate() + "." + date.getMonth()+1 + "." + date.getFullYear();
			}, {immediate: true, deep: true});
			return {
				topLeftString
			}
		}
	}
</script>

<style scoped>
.calendarDay {
	border: solid 1px #0002;
	min-width: 64px;
	min-height: 64px;
	border-radius: 6px;
	transition: 0.2s ease;
	padding: 8px;
    min-height: 0;
	display: flex;
	flex-direction: column;
	gap: 6px;
}
.calendarDay:hover {
	box-shadow: 0 2px 4px #0004;
}
.calendarDayNumber {
	font-weight: bold;
	font-size: 1.5em;
}
.calendarDayTop {
	display: flex;
	flex-direction: row;
	gap: 6px;
}
.calendarDayEventList {
	display: flex;
	flex-direction: column;
	gap: 6px;
	overflow: auto;
    min-height: 0;
}
.calendarDayEventItem {
	display: flex;
	gap: 6px;
	width: 100%;
}
textarea {
	flex-grow: 1;
}
</style>