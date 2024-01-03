<template>
	<div id="sidebarLogo">
		<div class="snow"></div>
		<div id="sidebarLogo_inner">
			<img id="sidebarLogo_icon" src="@/assets/images/logo_small_mono_2.svg" alt="">
			<img id="sidebarLogo_text" src="@/assets/images/logo_text.svg" alt="">
		</div>
	</div>
</template>

<script>
export default {
	name: 'SidebarLogo'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@keyframes sidebarLogo_inner {
	0% {
		opacity: 0;
		transform: translateY(16px);
	}
	100% {
		opacity: 1;
		transform: translateY(0);
	}
}

@keyframes sidebarLogo_text {
	0% {
		transform: translateX(0);
		width: 98px;
	}
	100% {
		transform: translateX(-32px);
		width: 0;
		opacity: 0;
	}
}

#sidebarLogo {
	font-weight: bold;
	font-size: 32px;
	height: 80px;
	flex-grow: 0;
	flex-shrink: 0;
	color: #fff;
	background: linear-gradient(30deg, #12358e, #057182);
	background: linear-gradient(30deg, #22459e, #45b0de);
	text-align: center;
	padding: 8px 16px;
	display: flex;
	justify-content: center;
	align-items: center;
	overflow: hidden;
}

#sidebarLogo #sidebarLogo_inner {
	height: 50px;
	filter: invert(1);
	display: flex;
	justify-content: center;
	align-items: center;
	animation: sidebarLogo_inner 1s ease forwards 0.25s;
	opacity: 0;
}

#sidebarLogo #sidebarLogo_icon {
	height: 50px;
}

#sidebarLogo #sidebarLogo_text {
	height: 24px;
	width: 98px;
	margin-left: 8px;
	animation: sidebarLogo_text 0.5s ease forwards 1.5s;
}

body {
  background-color: #061123;
  height: 100vh;
  display: grid;
  justify-content: center;
  align-content: center;
}

.snow {
	position: absolute;
	width: 220px;
	height: 80px;
	background-image: url("data:image/svg+xml,%3Csvg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' viewBox='0 0 50 50' style='enable-background:new 0 0 50 50%3B' xml:space='preserve'%3E%3Cstyle type='text/css'%3E.st1%7Bopacity:0.3%3Bfill:%23FFFFFF%3B%7D.st3%7Bopacity:0.1%3Bfill:%23FFFFFF%3B%7D%3C/style%3E%3Ccircle class='st1' cx='5' cy='8' r='1'/%3E%3Ccircle class='st1' cx='38' cy='3' r='1'/%3E%3Ccircle class='st1' cx='12' cy='4' r='1'/%3E%3Ccircle class='st1' cx='16' cy='16' r='1'/%3E%3Ccircle class='st1' cx='47' cy='46' r='1'/%3E%3Ccircle class='st1' cx='32' cy='10' r='1'/%3E%3Ccircle class='st1' cx='3' cy='46' r='1'/%3E%3Ccircle class='st1' cx='45' cy='13' r='1'/%3E%3Ccircle class='st1' cx='10' cy='28' r='1'/%3E%3Ccircle class='st1' cx='22' cy='35' r='1'/%3E%3Ccircle class='st1' cx='3' cy='21' r='1'/%3E%3Ccircle class='st1' cx='26' cy='20' r='1'/%3E%3Ccircle class='st1' cx='30' cy='45' r='1'/%3E%3Ccircle class='st1' cx='15' cy='45' r='1'/%3E%3Ccircle class='st1' cx='34' cy='36' r='1'/%3E%3Ccircle class='st1' cx='41' cy='32' r='1'/%3E%3C/svg%3E");
	background-position: 0px 0px;
	animation: snowBG 20s linear infinite;
}

@keyframes snowBG {
  0% {
	background-position: 0 0;
  }
  100% {
	background-position: 0px 320px;
  }
}

</style>
