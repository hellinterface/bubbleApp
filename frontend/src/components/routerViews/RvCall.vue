<template>
	<div class="router-view-container" id="rvCall">
		<div class="routerView_mainContent">
			<CallView></CallView>
		</div>
	</div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore'
import CallView from '../CallView.vue';
import HbsCall from '../headerButtonSets/HbsCall.vue';
const headerTitle = "Собрание";
var mainStore;

export default {
	name: 'RvCalls',
    components: {
		CallView
    },
	mounted() {
		mainStore = useMainStore();
		mainStore.header.buttonSet = HbsCall;
		mainStore.header.title = headerTitle;
		console.log(mainStore.header.title);
	}
}
</script>

<style scoped>
#rvCall {
    height: 100%;
}
.routerView_mainContent {
    height: 100%;
}
.callView {
    height: 100%;
}
</style>
