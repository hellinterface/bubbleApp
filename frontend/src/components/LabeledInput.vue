<template>
    <div>
      <label :for="name"><slot></slot></label>
      <textarea v-if="type == 'textarea'" :name="name" :required="required" :placeholder="placeholder" :value="modelValue" @input="updateValue" @focus="onFocus" @blur="onBlur" ref="mainInputElement"></textarea>
      <input v-else :type="type" :name="name" :required="required" :placeholder="placeholder" :value="modelValue" @input="updateValue" @focus="onFocus" @blur="onBlur" ref="mainInputElement"/>
    </div>
</template>

<script>
    import { ref, onMounted } from 'vue';
    const mainInputElement = ref(null);
    export default {
        name: 'LabeledInput',
        props: {
            type: { default: "text", type: String },
            name: { default: "", type: String },
            required: { default: false, type: Boolean },
            placeholder: { default: "", type: String },
            modelValue: { default: "", type: String },
        },
        emits: ['update:modelValue', 'focus', 'blur'],
        setup(props, {emit}) {
            //const emit = defineEmits([])
            onMounted(() => {
            });
            const updateValue = (event) => {
                emit('update:modelValue', event.target.value)
            }
            const onFocus = (event) => {
                emit('focus', event)
            }
            const onBlur = (event) => {
                emit('blur', event)
            }
            return {
                mainInputElement,
                updateValue,
                onFocus,
                onBlur
            }
        },
        data() {
            return {
            }
        }
    }
</script>

<style scoped>
    div {
        display: flex;
        flex-direction: column;
    }
    label {
        font-weight: 500;
        font-size: 1.25em;
        margin-left: 0.8em;
        margin-bottom: 0.5em;
        color: #222;
    }
    input {
        padding: 10px 16px;
        font-size: 1.0em;
    }
</style>