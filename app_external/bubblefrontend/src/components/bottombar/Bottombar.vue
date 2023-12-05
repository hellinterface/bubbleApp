<template>
	<div id="bottombarContent">
		<BottombarCategoryLink icon_name="contacts" to="/app/contacts">Контакты</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="group" to="/app/groupview">Group view</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="groups_3" to="/app/grouplist">Группы</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="task_alt" to="/app/tasks">Задачи</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="calendar_month" to="/app/calendar">Календарь</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="forum" to="/app/chats">Диалоги</BottombarCategoryLink>
	</div>
</template>

<script>
import BottombarCategoryLink from './BottombarCategoryLink.vue';
export default {
	name: 'BottombarMain',
	components: {
		BottombarCategoryLink
	},
	props: {
		msg: String
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
	#bottombarContent {
		background-color: #fff;
		background: linear-gradient(#eff, #cef);
		width: 100%;
		height: 100%;
		border-radius: 4px;
		box-shadow: 0 4px 12px #0006;
		display: flex;
		gap: 6px;
		align-items: center;
		justify-content: center;
	}
</style>
