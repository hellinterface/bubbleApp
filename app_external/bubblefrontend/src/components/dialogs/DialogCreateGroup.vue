<template>
    <div>
        <LabeledInput type="text" name="title">Название</LabeledInput>
        <LabeledInput type="text" name="handle">Ссылка</LabeledInput>
        <XButton icon_name="done">Создать</XButton>
    </div>
</template>

<script>
import XButton from '@/components/elements/XButton.vue';
import LabeledInput from '@/components/LabeledInput.vue'

export default {
	name: 'DialogCreateView',
	components: {
        XButton,
        LabeledInput
	},
	mounted() {
	},
}
</script>

<style scoped>
</style>
