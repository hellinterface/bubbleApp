<template>
    <button @click="$emit('onclick')" :class="appearance">
        <icon v-if="icon_name != ''">{{ icon_name }}</icon>
        <div v-if="!!($slots.default)" class="button_label">
            <slot></slot>
        </div>
    </button>
</template>

<script>
	export default {
		name: 'XButton',
		props: {
			onclick: {
				default: () => {},
				type: Function
			},
            icon_name: {
                default: "",
                type: String
            },
            appearance: { // normal / outlined / small / round / red
                default: "normal",
                type: String
            }
		},
        setup() {

        }
	}
</script>

<style scoped>
button {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: center;
}
button.normal {
    color: #fff;
}
button.outlined {
    background: #fff;
    border: solid 1px var(--color-primary);
    color: var(--color-primary);
}
button.outlined:hover {
    background: var(--color-pale1);
    box-shadow: 0 2px 4px #0004;
}
button.outlined:active {
    background: var(--color-pale1);
    box-shadow: 0 0 3px #0004;
}
button.small {
    background: none;
    padding: 0;
    color: #0006;
}
button.small:hover {
    background: #0001;
}
button.round {
    border-radius: 50%;
    aspect-ratio: 1;
}
button.red {
    background: var(--color-red);
}
button.red:hover {
    background: var(--color-red-lighter);
}
button.red:pressed {
    background: var(--color-red-darker);
}
</style>