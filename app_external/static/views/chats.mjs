"use strict";

const id = "chats";

const template = `
<div class="innerView_header innerView_panel">
    <div class="innerView_header_picture"></div>
    <div class="innerView_header_title">Chats</div>
</div>
<div class="innerView_body">
    <div class="innerView_body_leftbar innerView_panel">
        <div class="chatList">
            <div class="chatEntry">
                <div class="chatEntry_top">
                    <div class="chatEntry_avatar"></div>
                    <div class="chatEntry_title">Chat 1</div>
                </div>
                <div class="chatEntry_lastMessage">21:30 Last message</div>
            </div>
        </div>
    </div>
    <div class="innerView_body_center innerView_panel"></div>
    <div class="innerView_body_rightbar innerView_panel"></div>
</div>
`;

function onLoad() {
}

export default {id, template, onLoad};