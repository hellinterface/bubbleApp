"use strict";

import groups from "/static/views/groups.mjs";
import groupview from "/static/views/groupview.mjs";
import chats from "/static/views/chats.mjs";
import calendar from "/static/views/calendar.mjs";
import contacts from "/static/views/contacts.mjs";
import tasks from "/static/views/tasks.mjs";
import settings from "/static/views/settings.mjs";

console.log("Bubble v0.0.1");
let rightSide = document.getElementById('rightSide');
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

function openUserInfoPage() {
    document.querySelector(".innerView_header").innerText = "User info";
    getCurrentUser().then(res2 => {
        console.log(res2);
        res2 = JSON.stringify(res2);
        document.querySelector(".innerView_body_center").innerText = "Your user info: \n\n" + res2;
    });
}

function applyUserDataToApp() {
    getCurrentUser().then(userdata => {
        sidebarBottom_userBar_visiblename.innerText = userdata.visiblename;
        sidebarBottom_userBar_handle.innerText = "@" + userdata.handle;
    });
}
applyUserDataToApp();

class dialogWindow {
    constructor(contentFilePath) {
        let elementWindow = document.createElement("div");
        elementWindow.className = "dialogWindow";
        let elementContent = document.createElement("div");
        elementContent.className = "dialogWindowContent";
        elementWindow.appendChild(elementContent);
        fetch(contentFilePath).then(res => { return res.text() }).then(res2 => {
            elementContent.innerHTML = res2;
            document.body.appendChild(elementWindow);
        });
    }
}

function createTestDialogWindow() {
    let testDialog = new dialogWindow("/static/dialogues/test.html");
}

/*
innerView_groupList.addEventListener('scroll', () => {
    console.log(innerView_groupList.scrollTop);
    if (innerView_groupList.scrollTop > 80) {
        innerView_groupList.classList.add('scrolledEnough');
    }
    else {
        innerView_groupList.classList.remove('scrolledEnough');
    }
});
*/

const routes = {
    "": { title: "Home", module: groups },
    "groups": { title: "groupList", module: groups },
    "groupview": { title: "groupview", module: groupview },
    "calendar": { title: "Calendar", module: calendar },
    "chats": { title: "Chats", module: chats },
    "contacts": { title: "Contacts", module: contacts },
    "tasks": { title: "Tasks", module: tasks },
    "settings": { title: "Settings", module: settings },
};

console.log(routes);

function router() {
    let pathname = window.location.pathname;
    console.warn(pathname);
    let view = routes[pathname.split('/')[2]];

    if (view) {
        console.log("FOUND VIEW", view.module.id);
        document.title = view.title;
        let parentContainer = document.createElement('div');
        parentContainer.classList.add("innerView")
        parentContainer.id = "innerView_" + view.module.id;
        console.log(view.module.template)
        parentContainer.innerHTML = view.module.template;
        rightSide.innerHTML = "";
        rightSide.appendChild(parentContainer);
    }
    else {
        console.log("NOT FOUND VIEW");
        history.replaceState("", "", "/app");
        //router();
    }
};

[...sidebarCategory_mainLinks.children].forEach(element => {
    element.addEventListener('click', () => {
        console.log(location.hostname + "/app/" + element.getAttribute("bb-view-link"));
        history.pushState("", "", window.location.origin + "/app/" + element.getAttribute("bb-view-link"));
        router();
    })
});

window.addEventListener("popstate", router);
window.addEventListener("DOMContentLoaded", router);

function userEditTest() {
    let obj = {
        id: "PmU-2aeT",
        handle: "new_handle_eee"
    };
    fetch('/api/users/edit', {
        method: "POST",
        body: JSON.stringify(obj)
    }).then(res1 => res1.json()).then(res2 => console.log(res2));
}

useredittest_button.onclick = userEditTest;