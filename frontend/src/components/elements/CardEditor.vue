<template>
	<div class="cardEditor" ref="ROOT">
		<LabeledInput>Название</LabeledInput>
		<LabeledInput type="textarea">Описание</LabeledInput>
		<LabeledInput>Цвет</LabeledInput>
	</div>
</template>

<script>
import { ref } from 'vue';
const ROOT = ref(null);

function hexColorAdd(input, to_add) {
	let rgb;
	if (input.length == 4) {
		rgb = [input[1]+input[1], input[2]+input[2], input[3]+input[3]];
	}
	else {
		rgb = [input.slice(1,3), input.slice(3,5), input.slice(5,7)];
	}
	let output = "#";
	for (let color of rgb) {
		let x = parseInt(Number("0x" + color), 10);
		x = x + to_add;
		if (x < 0) x = 0;
		if (x > 255) x = 255;
		x = x.toString(16);
		if (x.length < 2) x = "0" + x;
		output += x;
	}
	return output;
}

import LabeledInput from '../LabeledInput.vue';
	export default {
		name: 'CardEditor',
		components: {
			LabeledInput
		},
		props: {
			cardObject: {
				type: Object
			}
		},
		watch: {
			cardObject(newVal, oldVal) {
				console.log(newVal, oldVal);
				if (newVal.color) {
					ROOT.value.style.background = `linear-gradient(${newVal.color}, ${hexColorAdd(newVal.color, -60)})`
				}
				else {
					ROOT.value.style.background = "linear-gradient(#ccc, #aaa)";
				}
			}
		},
		setup() {
			return {
				ROOT
			}
		}
	}
</script>

<style scoped>
.cardEditor {
	border: solid 1px #0002;
	border-radius: 6px;
	transition: 0.2s ease;
	padding: 8px;
	background: plum;
	width: 100%;
}
</style>