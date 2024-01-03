<template>
	<div id="bottombarContent">
		<BottombarCategoryLink icon_name="contacts" to="/contacts">Контакты</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="groups_3" to="/grouplist">Группы</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="task_alt" to="/tasks">Задачи</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="calendar_month" to="/calendar">Календарь</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="forum" to="/chats">Диалоги</BottombarCategoryLink>
		<BottombarCategoryLink icon_name="folder" to="/files">Файлы</BottombarCategoryLink>
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
