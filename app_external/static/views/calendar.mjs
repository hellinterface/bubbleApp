"use strict";

const id = "calendar";

const template = `
<div class="innerView_header innerView_panel">
    <div class="innerView_header_title">Календарь</div>
</div>
<div class="innerView_body">
    <div class="innerView_body_leftbar innerView_panel"></div>
    <div class="innerView_body_center innerView_panel">
        <div class="calendar_mainView_month">
        </div>
    </div>
</div>
`;
function onLoad() {
    let view = document.querySelector('.calendar_mainView_month');
}

export default {id, template, onLoad};