
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
	<div class="dialogWrapper" ref="dialogWrapper"></div>
</template>

<script>
	import { inject, ref, createApp } from 'vue'
	import axios from 'axios';
	import SidebarMain from '@/components/sidebar/Sidebar.vue'
	import RightMainHeader from '@/components/RightMainHeader.vue'
	import BottombarMain from '@/components/bottombar/Bottombar.vue'
	import { MqResponsive } from 'vue3-mq'
	import { useRouter, useRoute } from 'vue-router'
	import { useMainStore } from '@/stores/mainStore'
	import ContextMenu from '@/components/contextmenu/ContextMenu.vue'
	import DialogWindow from '@/components/DialogWindow.vue'

	const ROOT = ref(null);
	const dialogWrapper = ref(null);

	export default {
		name: 'App',
		components: {
			ContextMenu,
			MqResponsive,
			SidebarMain,
			BottombarMain,
			RightMainHeader,
		},
		methods: {},
		setup() {
			const defaultUser = {"handle": "NOT_LOGGED_IN", "visible_name": "! АНОН !", "email": "no_email"};
			const mainStore = useMainStore();

			const $cookies = inject('$cookies');
			let token = $cookies.get('access_token');
			console.log(token);
			mainStore.root = {
				showDialogWindow(dialogFragment, propsObject = {}) {
					console.log("WOOOOOOOOOOOOOOOOOOOOOOOOOOOOO DIALOG");
					console.log(dialogFragment);
					propsObject.fragment = dialogFragment;
					let dialog = createApp(DialogWindow, propsObject);
					//dialog.setFragment(dialogFragment);
					console.log(dialog);
					dialog.mount(dialogWrapper.value);
				}
			};
			console.log('+++++++++++++++++++++++++++');
			console.log(mainStore.root);
			console.log('+++++++++++++++++++++++++++');
			mainStore.currentUser = defaultUser;
			if (!token) {
				//window.location.href = "/login";
				mainStore.currentUser = defaultUser;
			}
			else {
				mainStore.accessToken = token;
				console.warn("GETTING ME");
				axios.get("http://127.0.0.1:7070/api/users/me", {headers: {"X-Access-Token": token}}).then(res => {
					mainStore.currentUser = res.data;
					console.warn("ME", res);
					sidebarKey.value += 1;
				})
				.catch(err => {
					console.error("ME", err);
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
				sidebarKey,
				dialogWrapper
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