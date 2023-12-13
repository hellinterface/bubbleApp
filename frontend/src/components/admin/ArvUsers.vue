<template>
	<div class="router-view-container" id="arvUsers">
		<div class="sqlQueryInputContainer">
			<input type="text" class="sqlQueryInput" placeholder="SQL Query" ref="sqlQueryInput" />
			<XButton icon_name="send" @onclick="makeQuery()"></XButton>
		</div>
		<div class="tableContainer">
			<table>
				<thead>
					<td>ID</td>
					<td>Handle</td>
					<td>Visible name</td>
					<td>Email</td>
					<td>Join date</td>
					<td>Folder ID</td>
				</thead>
				<tr v-for="user in userList" :key="user.id">
					<td>{{user.id}}</td>
					<td>{{user.handle}}</td>
					<td>{{user.visible_name}}</td>
					<td>{{user.email}}</td>
					<td>{{user.join_date}}</td>
					<td>{{user.folder_id}}</td>
				</tr>
			</table>
		</div>
	</div>
</template>
<script>
import { ref } from 'vue'
import { useMainStore } from '@/stores/mainStore'
import XButton from '@/components/elements/XButton.vue'
import axios from 'axios';
const headerTitle = "Пользователи";
var mainStore;


export default {
	name: 'ArvUsers',
	components: {
		XButton
	},
	setup() {
		const userList = ref([]);
		const sqlQueryInput = ref(null);
		function makeQuery() {
			console.log(sqlQueryInput.value.value);
			axios.post('http://localhost:7070/api/users/get_query', {query: sqlQueryInput.value.value})
			.then(function (response) {
				console.log(response);
				userList.value = response.data;
			})
			.catch(function (error) {
				console.log(error);
			});
		}
		return {
			makeQuery,
			sqlQueryInput,
			userList
		}
	},
	mounted() {
		mainStore = useMainStore();
		mainStore.currentRightHeaderTitle = headerTitle;
		console.log(mainStore.currentRightHeaderTitle);
	},
	data() {
		return {
		}
	}
}
</script>

<style scoped>
.router-view-container {
	background: #fff;
	height: 100%;
	border-radius: 6px;
	padding: 8px;
	max-height: 100%;
	overflow: hidden;
}
.tableContainer {
	height: 100%;
	overflow: auto;
}
table {
	border-collapse: collapse;
	width: 100%;
}
td {
	border-bottom: solid 1px #0004;
	padding: 6px 10px;
}
thead {
	font-weight: bold;
	color: #000a;
}
.sqlQueryInputContainer {
	display: flex;
	gap: 6px;
}
.sqlQueryInput {
	flex-grow: 1;
}
</style>
