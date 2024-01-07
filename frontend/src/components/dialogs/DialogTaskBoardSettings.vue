<template>
    <div class="dialogContent_container">
        <LabeledInput type="text" name="title" v-model="input_title_value">Название группы</LabeledInput>
        <!-- get all contacts and all owned groups in a list -->
        <!-- public toggles -->

        <XButton icon_name="save" @click="save()">Сохранить</XButton>
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
var board_id_ref = ref(-1);

export default {
	name: 'DialogTaskBoardSettings',
	components: {
        XButton,
        LabeledInput
	},
    props: {
        board_id: {
            type: Number
        }
    },
    methods: {
        save() {
            console.log(board_id_ref.value);
            console.log(input_title_value.value, this.board_id);
            axios.post(location.protocol+"//"+location.hostname+":7070/api/tasks/getBoardById",
            {},
            {withCredentials: true})
            .then(res => console.log(res))
            .catch(err => console.log(err));
        }
    },
	mounted() {
        console.warn("MOUNTED DIALOG FRAGMENT");
        console.log(this.board_id);
        console.log(this.$props);
        axios.get(location.protocol+"//"+location.hostname+":7070/api/tasks/getBoardById/"+board_id_ref.value,
            {withCredentials: true})
        .then(res => {
            console.log(res);
            input_title_value.value = res.data.title;
        })
        .catch(err => console.log(err));
	},
    setup(props) {
        input_title_value.value = "";
        //mainStore = useMainStore();
        console.warn("SETUP DIALOG FRAGMENT");
        board_id_ref = toRefs(props).board_id;
        return {
            input_title_value,
            board_id_ref
        }
    },
    data() {
    }
}
</script>

<style scoped>
.dialogContent_container {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
</style>
