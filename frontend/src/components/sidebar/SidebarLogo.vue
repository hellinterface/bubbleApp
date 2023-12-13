<template>
	<div id="sidebarLogo">
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
</style>
