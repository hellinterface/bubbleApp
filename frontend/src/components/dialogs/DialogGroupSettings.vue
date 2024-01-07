<template>
    <div class="gialogCreateSetup_container">
        <LabeledInput type="text" name="title" v-model="input_title_value">Название группы</LabeledInput>
        <LabeledInput type="text" name="title" v-model="input_title_value">Название группы</LabeledInput>
        <LabeledInput type="text" name="title" v-model="input_title_value">Название группы</LabeledInput>
        <LabeledInput type="text" name="title" v-model="input_title_value">Название группы</LabeledInput>
        <XButton icon_name="done" @click="createChannel()">Создать</XButton>
    </div>
</template>

<script>
import { ref, toRefs } from 'vue';
import XButton from '@/components/elements/XButton.vue';
import LabeledInput from '@/components/LabeledInput.vue'
import axios from 'axios';
//import { useMainStore } from '@/stores/mainStore';

//var mainStore;
const input_title_value = ref("");
var group_id_ref = ref("");

export default {
	name: 'DialogGroupSettings',
	components: {
        XButton,
        LabeledInput
	},
    props: {
        group_id: {
            type: Number
        }
    },
    methods: {
        createChannel() {
            console.log(group_id_ref.value);
            console.log(input_title_value.value, this.group_id);
            axios.post(location.protocol+"//"+location.hostname+":7070/api/groups/createChannel",
            {title: input_title_value.value, group_id: this.group_id, private: false},
            {withCredentials: true})
            .then(res => console.log(res))
            .catch(err => console.log(err));
        }
    },
	mounted() {
        console.warn("MOUNTED DIALOG FRAGMENT");
        console.log(this.group_id);
        console.log(this.$props);
	},
    setup(props) {
        input_title_value.value = "";
        //mainStore = useMainStore();
        console.warn("SETUP DIALOG FRAGMENT");
        group_id_ref = toRefs(props).group_id;
        return {
            input_title_value
        }
    },
    data() {
    }
}
</script>

<style scoped>
.gialogCreateSetup_container {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
</style>
