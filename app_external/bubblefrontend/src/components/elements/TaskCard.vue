<template>
    <div class="taskCard" ref="ROOT">
		<div class="taskCardTitle">{{ card_object.title }}</div>
		<div class="taskCardDescription" v-if="card_object.description">{{ card_object.description }}</div>
    </div>
</template>

<script>
	import { ref, toRefs, onMounted } from 'vue';
	export default {
		name: 'TaskCard',
		props: {
			card_object: {
				type: Object
			},
		},
		setup(props) {
			const ROOT = ref(null);
			const { card_object } = toRefs(props);
			onMounted(() => {
				console.log(ROOT.value);
				if (card_object.value?.color) {
					ROOT.value.style.background = card_object.value.color;
				}
			});
			return {
				ROOT
			}
		}
	}
</script>

<style scoped>
.taskCard {
	background-color: #79e;
	box-shadow: 0 2px 4px #0004;
	border-radius: 4px;
	color: white;
	padding: 8px;
}

.taskCardTitle {
	font-weight: bold;
}
</style>