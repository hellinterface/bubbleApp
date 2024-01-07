<template>
	<div class="errorMessage">
        <div class="errorMessage_icon"><icon>warning</icon></div>
        <div class="errorMessage_content">
            {{ message }}
        </div>
	</div>
</template>

<script>

export default {
	name: 'ErrorMessage',
	components: {
	},
    props: {
        message: {
            type: String,
            default: "Произошла ошибка."
        }
    },
    methods: {
    },
    setup() {

    },
	mounted() {
	}
}
</script>

<style scoped>
.errorMessage {
    background: var(--color-red);
    border: solid 1px #833;
    box-shadow: 0 2px 4px #0003;
    border-radius: 6px;
    display: flex;
    flex-direction: row;
    gap: 8px;
    padding: 8px;
    height: 48px;
    align-items: center;
    color: #fff;
}
.errorMessage_icon {
    margin-top: 3px;
}
</style>
