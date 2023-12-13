<template>
    <a v-if="isExternalLink" v-bind="$attrs" :href="to" target="_blank">
        <slot />
    </a>
    <router-link v-else v-bind="$props">
        <slot />
    </router-link>
</template>

<script>
    import {
        RouterLink
    } from 'vue-router'

    export default {
        name: 'BBRouterLink',
        inheritAttrs: false,

        props: {
            //to: String,
            ...RouterLink.props
        },

        computed: {
            isExternalLink() {
                return typeof this.to === 'string' && this.to.startsWith('http')
            },
        },
    }
</script>