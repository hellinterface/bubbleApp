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
                <div class="settings_entryTitle">Handle</div>
            </div>
            <div class="settings_entryRight">
                <input type="text" placeholder"Handle" />
            </div>
        </div>
    </div>
</div>
`;

export default {id, template};