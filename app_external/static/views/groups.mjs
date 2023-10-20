"use strict";

const id = "groups";

const template = `
<div class="groupList_header">
    <div class="groupList_headerContent">Your groups</div>
    <div class="groupList_headerBackground"></div>
</div>
<div class="groupList_list">
    <div class="groupList_card">
        <div class="groupList_avatar"></div>
        <div class="groupList_title">Group 1</div>
        <div class="groupList_moreMenuButton"><icon>more_vert</icon></div>
    </div>
    <div class="groupList_card">
        <div class="groupList_avatar"></div>
        <div class="groupList_title">Group 2</div>
        <div class="groupList_moreMenuButton"><icon>more_vert</icon></div>
    </div>
</div>
`;

export default {id, template};