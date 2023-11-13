
<template>
	<div id="appContainer" ref="ROOT">
		<MqResponsive target="md+" class="no-shrink-flex">
			<div id="sidebar">
				<!--<button @click="() => showDialogWindow()">Показать диалоговое окно</button>-->
				<SidebarMain :key="sidebarKey"></SidebarMain>
			</div>
		</MqResponsive>
		<div id="rightSide">
			<RightMainHeader :currentTitle="mainStore.currentRightHeaderTitle" :currentButtonSet="mainStore.currentRightHeaderButtonSet"></RightMainHeader>
			<div id="rightSide_mainContainer">
				<router-view></router-view>
			</div>
		</div>
		<MqResponsive target="sm-">
			<div id="bottombar">
				<BottombarMain></BottombarMain>
			</div>
		</MqResponsive>
	</div>
	<ContextMenu ref="contextMenu"></ContextMenu>
	<DialogWindow style="display: none">
		<DialogCreateGroup></DialogCreateGroup>
	</DialogWindow>
</template>

<script>
	import { inject, ref } from 'vue'
	import axios from 'axios';
	import SidebarMain from '@/components/sidebar/Sidebar.vue'
	import RightMainHeader from '@/components/RightMainHeader.vue'
	import BottombarMain from '@/components/bottombar/Bottombar.vue'
	import { MqResponsive } from 'vue3-mq'
	import { useRouter, useRoute } from 'vue-router'
	import { useMainStore } from '@/stores/mainStore'
	import ContextMenu from '@/components/contextmenu/ContextMenu.vue'
	import DialogWindow from '@/components/DialogWindow.vue'
	import DialogCreateGroup from '@/components/dialogs/DialogCreateGroup.vue'

	const ROOT = ref(null);

	export default {
		name: 'App',
		components: {
			ContextMenu,
			MqResponsive,
			SidebarMain,
			BottombarMain,
			RightMainHeader,
			DialogWindow, DialogCreateGroup
		},
		methods: {
			showDialogWindow() {
				let dialog = new DialogWindow();
				ROOT.value.appendChild(dialog);
			}
		},
		setup() {
			const defaultUser = {"handle": "NOT_LOGGED_IN", "visible_name": "! АНОН !", "email": "no_email"};
			const mainStore = useMainStore();

			const $cookies = inject('$cookies');
			let token = $cookies.get('access_token');
			console.log(token);
			mainStore.currentUser = defaultUser;
			if (!token) {
				//window.location.href = "/login";
				mainStore.currentUser = defaultUser;
			}
			else {
				console.warn("GETTING ME");
				axios.get("http://127.0.0.1:7070/api/users/me", {headers: {"X-Access-Token": token}}).then(res => {
					console.log(mainStore.currentUser);
					mainStore.currentUser = res.data;
					console.log(res);
					console.log(mainStore.currentUser);
					sidebarKey.value += 1;
				})
				.catch(err => {
					console.error(err);
					mainStore.currentUser = defaultUser;
				})
			}

			const router = useRouter();
			const route = useRoute();
			console.log(router, route);

			const sidebarKey = ref(0);
			const contextMenu = ref(null);
			console.log(contextMenu);
			mainStore.contextMenu = contextMenu;
			return {
				contextMenu,
				ROOT,
				sidebarKey
			}
		},
		mounted() {
			console.log("App.vue mounted")
		},
		data() {
			const mainStore = useMainStore();
			console.log(mainStore);
			return {
				mainStore
			}
		}
	}
</script>

<style>
	#appContainer {
		height: 100%;
		width: 100%;
		display: flex;
		max-width: 100%;
		max-height: 100%;
		padding: 6px;
		gap: 6px;
	}

	#sidebar {
		height: 100%;
		width: 15vw;
		min-width: 220px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		z-index: 20;
		flex-shrink: 0;
		gap: 6px;
	}

	#rightSide {
		flex-grow: 1;
		border-radius: 6px;
		z-index: 18;
		display: flex;
		gap: 6px;
		flex-direction: column;
	}

	#rightSide_mainContainer {
		flex-grow: 1;
	}

	#bottombar {
		height: 64px;
		width: 100%;
	}

	.no-shrink-flex {
		flex-shrink: 0;
		display: flex;
	}

	@media (max-width: 767px) {
		#appContainer {
			flex-direction: column;
		}
		#sidebar {
			height: 64px;
			width: 100%;
		}
		#sidebarLogo {
			display: none;
		}
	}
</style>