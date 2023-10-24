"use strict";

const id = "calendar";

const template = `
<div class="innerView_header innerView_panel">
    <div class="innerView_header_title">Настройки</div>
</div>
<div class="innerView_body">
    <div class="innerView_body_leftbar innerView_panel"></div>
    <div class="innerView_body_center innerView_panel">
        <div class="settings_entry">
            <div class="settings_entryLeft">
                <div class="settings_entryTitle">Имя пользователя</div>
            </div>
            <div class="settings_entryRight">
                <input type="text" placeholder="Имя пользователя" />
            </div>
        </div>
        <div class="settings_entry">
            <div class="settings_entryLeft">
                <div class="settings_entryTitle">Публичное имя</div>
            </div>
            <div class="settings_entryRight">
                <input type="text" placeholder="Публичное имя" />
            </div>
        </div>
        <div class="settings_entry">
            <div class="settings_entryLeft">
                <div class="settings_entryTitle">Почта</div>
            </div>
            <div class="settings_entryRight">
                <input type="text" placeholder="Почта" />
            </div>
        </div>
    </div>
</div>
`;

async function getCurrentUser() {
    try {
        let res = await fetch(window.location.origin + "/api/users/me");
        console.log(res);
        if (res.status >= 400 && res.status <= 600) {
            throw new Error("Error " + res.status);
        }
        res = await res.json();
        return res;
    }
    catch (error) {
        console.log(error);
    }
}

function applyUserDataToApp() {
    getCurrentUser().then(userdata => {
        console.log("YEAP");
        sidebarBottom_userBar_visiblename.innerText = userdata.visible_name;
        sidebarBottom_userBar_handle.innerText = "@" + userdata.handle;
    });
}

function onLoad() {
    applyUserDataToApp();
}

export default {id, template, onLoad};