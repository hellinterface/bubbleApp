<template>
    <div>
      <label :for="name"><slot></slot></label>
      <input :type="type" :name="name" :required="required" :placeholder="placeholder" :value="value"/>
    </div>
</template>

<script>
    export default {
        name: 'LabeledInput',

        props: {
            type: { default: "text", type: String },
            name: { default: "", type: String },
            required: { default: false, type: Boolean },
            placeholder: { default: "", type: String },
            value: { default: "", type: String },
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