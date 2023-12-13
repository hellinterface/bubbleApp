<template>
    <div class="calendarDay">
        <div class="calendarDay_number">{{ day_number }}</div>
    </div>
</template>

<script>
	export default {
		name: 'CalendarDay',

		props: {
			day_number: {
				default: 0,
				type: Number
			},
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
}
.calendarDay:hover {
	box-shadow: 0 2px 4px #0004;
}
.calendarDay_number {
    font-weight: bold;
    font-size: 1.5em;
}
</style>