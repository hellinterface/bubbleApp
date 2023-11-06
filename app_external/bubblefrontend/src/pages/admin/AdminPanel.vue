
<template>
	<div id="appContainer">
		<MqResponsive target="md+" class="no-shrink-flex">
			<div id="sidebar">
				<AdminSidebar></AdminSidebar>
			</div>
		</MqResponsive>
		<div id="rightSide">
			<RightMainHeader :currentTitle="mainStore.currentRightHeaderTitle"></RightMainHeader>
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
</template>

<script>
	import { inject, ref } from 'vue'
	import AdminSidebar from '@/components/admin/AdminSidebar.vue'
	import RightMainHeader from '@/components/RightMainHeader.vue'
	import BottombarMain from '@/components/bottombar/Bottombar.vue'
	import { MqResponsive } from 'vue3-mq'
	import { useRouter, useRoute } from 'vue-router'
	import { useMainStore } from '@/stores/mainStore'
	import ContextMenu from '@/components/contextmenu/ContextMenu.vue'

	export default {
		name: 'AdminPanel',
		components: {
			ContextMenu,
			MqResponsive,
			AdminSidebar,
			BottombarMain,
			RightMainHeader
		},
		methods: {
			onClick (text) {
				alert(`You clicked ${text}!`);
			}
		},
		setup() {
			const $cookies = inject('$cookies');
			console.log($cookies.get('access-token'));
			/*
			if (!$cookies.get('access-token')) {
				window.location.href = "/login";
			}
			*/

			const router = useRouter();
			const route = useRoute();
			console.log(router, route);

			const contextMenu = ref(null);
			const mainStore = useMainStore();
			console.log(contextMenu);
			mainStore.contextMenu = contextMenu;
			return {
				contextMenu
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