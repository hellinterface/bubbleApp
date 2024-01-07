<template>
	<div class="cardEditor" ref="ROOT" :style="{background: `linear-gradient(${cardObjectRef.color}, ${hexColorAdd(cardObjectRef.color, -60)})`}">
		<LabeledInput :modelValue="cardObjectRef.title" @blur="(event) => {cardObjectRef.title = event.target.value}">Название</LabeledInput>
		<LabeledInput :modelValue="cardObjectRef.description" type="textarea" @blur="(event) => {cardObjectRef.description = event.target.value}">Описание</LabeledInput>
		<LabeledInput :modelValue="cardObjectRef.color" @blur="(event) => {cardObjectRef.color = event.target.value}" ref="input_color">Цвет</LabeledInput>
		<div class="cardEditorButtons">
			<XButton class="deleteButton" icon_name="delete" appearance="small">Удалить</XButton>
			<XButton class="addFileButton" icon_name="add" appearance="small">Добавить файл</XButton>
			<XButton class="managePermissionsButton" icon_name="person" appearance="small">Управление правами</XButton>
			<XButton class="saveButton" icon_name="save" appearance="small" @click="saveCard()">Сохранить</XButton>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';
import LabeledInput from '../LabeledInput.vue';
import XButton from './XButton.vue';

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


	export default {
		name: 'CardEditor',
		components: {
			LabeledInput,
			XButton
		},
		props: {
			cardObject: {
				type: Object
			}
		},
		setup(props) {
			var defaultCardObject = {color: "#666", title: "", description: ""};
			const ROOT = ref(null);
			const cardObjectRef = ref(defaultCardObject);
			const input_color = ref(null);
			const value_color = ref("#eee");
			const untouchedCardObject = ref(defaultCardObject);
			function refresh() {
				if (cardObjectRef.value.color) {
					ROOT.value.style.background = `linear-gradient(${cardObjectRef.value.color}, ${hexColorAdd(cardObjectRef.value.color, -60)})`
				}
				else {
					ROOT.value.style.background = "linear-gradient(#ccc, #aaa)";
				}
			}
			function saveCard() {
				/*
			    id: int
			    title: Optional[str]
			    description: Optional[str]
			    column_id: Optional[int]
			    position_y: Optional[int]
			    color: Optional[str]
			    owner_id: Optional[int]
			    deadline: Optional[int]
			    attached_files: Optional[list[int]]
				 */
				axios.post(location.protocol+"//"+location.hostname+":7070/api/tasks/updateCard",
				{id: cardObjectRef.value.id, title: cardObjectRef.value.title, description: cardObjectRef.value.description, color: cardObjectRef.value.color, attachedFiles: []},
				{withCredentials: true})
				.then(res => {
					console.log(res);
				})
				.catch(err => {
					console.log(err);
				})
			}
			watch(() => props.cardObject, (newValue, oldValue) => {
				console.log("XXXXXXXXXXXXXXXXXX");
				console.log(newValue, oldValue);
				cardObjectRef.value = props.cardObject;
				untouchedCardObject.value = structuredClone(props.cardObject);
			}, {immediate: true});

			onMounted(() => {
			});
			return {
				ROOT,
				cardObjectRef,
				refresh,
				input_color,
				value_color,
				hexColorAdd,
				untouchedCardObject,
				saveCard
			}
		}
	}
</script>

<style scoped>
.cardEditor {
	border: solid 1px #0002;
	border-radius: 6px;
	transition: 0.2s ease;
	padding: 6px;
	background: plum;
	width: 100%;
	display: flex;
	flex-direction: column;
	gap: 6px;
}

button {
	padding: 8px !important;
	color: #000 !important;
}

.cardEditorButtons {
	display: flex;
	flex-direction: column;
	gap: 6px;
	background: white;
	border-radius: 6px;
	padding: 6px;
}
</style>