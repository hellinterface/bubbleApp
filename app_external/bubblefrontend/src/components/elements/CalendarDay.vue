<template>
    <div class="calendarDay">
        <div class="calendarDay_number">{{ day_nubmer }}</div>
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
}
.calendarDay_number {
    font-weight: bold;
    font-size: 1.5em;
}
</style>