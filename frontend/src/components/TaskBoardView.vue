<template>
	<div class="taskBoardView" ref="ROOT">
        <div class="taskBoard_columnList">
            <TaskColumn v-for="column in columnList" :key="column.id" :column_object="column" @cardClick="(element, event, component) => dragElement(element, event, component)"></TaskColumn>
        </div>
        <div class="taskBoard_cardEditorContainer">
            <CardEditor :cardObject="selectedCardObject"></CardEditor>
        </div>
	</div>
</template>

<script>
import { ref } from 'vue'
import TaskColumn from '@/components/elements/TaskColumn.vue'
import CardEditor from '@/components/elements/CardEditor.vue'

const selectedCardObject = ref(null);

const columnList = ref([
    {id: "123", position_x: 0, title: "first column", cards: [
        {id: "123", position_y: 0, title: "cardtitle", description: "desc 123", color: "#89a"},
        {id: "234", position_y: 1, title: "card desc", description: "desc 123"},
        {id: "345", position_y: 2, title: "card color", color: "#aa7"},
    ]},
    {id: "234", position_x: 1, title: "second column", cards: [
    ]},
    {id: "345", position_x: 2, title: "third column", cards: [
        {id: "123", position_y: 0, title: "cardtitle", description: "desc 123", color: "#89a"},
        {id: "234", position_y: 1, title: "card desc", description: "desc 123"},
    ]},
    {id: "456", position_x: 3, title: "fourth column", cards: [
        {id: "123", position_y: 0, title: "cardtitle", description: "desc 123", color: "#89a"},
    ]},
]);

const ROOT = ref(null);

export default {
	name: 'TaskBoardView',
	components: {
        TaskColumn,
        CardEditor
	},
    methods: {
        dragElement: (drag, event, component) => {
            console.log("DRAG", drag, event);
            let originalParent;
            let innerX = 0, innerY = 0;
            let first_X = 0, first_Y = 0;
            let dragStarted = false;
            dragMouseDown(event);

            let deckElements = [...ROOT.value.children];
            let deckCardLineElements = [];
            deckElements.forEach(element => deckCardLineElements.push(element.querySelector('.taskColumnCardList')));

            function dragMouseDown(event) {
                event.preventDefault();
                //console.log(event.target.tagName);
            
                if (event.button == 2) {
                    document.onpointerup = () => onRightClick(event);
                }
                if (event.button == 0 && event.target.tagName != 'A' && !drag.deleted) {
                    originalParent = drag.parentElement;
                
                    let rect = drag.getBoundingClientRect();
                    innerX = event.clientX - rect.left;
                    innerY = event.clientY - rect.top;
                    console.log(innerX, innerY);
                    first_X = event.clientX;
                    first_Y = event.clientY;
                    dragStarted = false;
                
                    document.onpointerup   = closeDragElement;
                    document.onpointermove = elementDrag;
                }
            }

            function onRightClick(event) {
                event.preventDefault();
                document.onpointerup = null;
            }

            function elementDrag(event) {
                event.preventDefault();
                if (dragStarted == false && (Math.abs(first_X-event.clientX) > 8 || Math.abs(first_Y-event.clientY) > 8)) {
                    drag.style.width = drag.offsetWidth + "px";
                    drag.classList.add('card-dragging');
                    document.body.classList.add('dragging');
                    dragStarted = true;
                }
            
                //drag.style.transform = `translate(${event.clientX}px, ${event.clientY}px)`
                drag.style.top  = event.clientY + "px";
                drag.style.left = event.clientX - 120 + "px";
            
            }

            function closeDragElement(event) {
                if (dragStarted == true) {
                    let target;
                    if (event.pointerType == "mouse") {
                        target = event.target
                    }
                    else if (event.pointerType == "touch") {
                        target = document.elementFromPoint(event.clientX, event.clientY);
                    }
                    console.warn(event);
                    console.warn(event.target);
                    if (target.className == "taskColumn") {
                        target.querySelector(".taskColumnCardList").appendChild(drag);
                    }
                    else if (target.className == "taskColumnCardList") {
                        //let indexOfDeck = deckElements.indexOf(target.parentElement);
                        target.appendChild(drag);
                    }
                    else if (target.className == "taskCardInsert") {
                        target.parentElement.insertAdjacentElement('beforebegin', drag);
                    }
                    else {
                        originalParent.appendChild(drag);
                    }
                }
                else {
                    console.log(component);
                    selectedCardObject.value = component.card_object;
                }
            
                // Let positioning of the card to the CPU. Also remove the dragging class.
                drag.style.top = 'auto'; drag.style.left = 'auto';
                //drag.style.transform = 'translate(0, 0)';
                drag.classList.remove('card-dragging');
                document.body.classList.remove('dragging');
                drag.style.width = "100%";
            
                document.onpointermove = null;
                document.onpointerup = null;
            
            }
        }
    },
    setup() {
        return {
            columnList,
            ROOT,
            selectedCardObject
        }
    }
}
</script>

<style scoped>
.taskBoardView {
    display: flex;
    flex-direction: row;
    height: 100%;
    gap: 6px;
    flex-grow: 1;
}

.taskBoard_cardEditorContainer {
    height: 100%;
}

.taskBoard_columnList {
    display: flex;
    flex-direction: row;
    height: 100%;
    gap: 6px;
    max-width: 100%;
    overflow: auto;
    flex-grow: 1;
}

.taskBoardView.dragging .taskCard:hover .taskCardInsert {
	height: 64px;
	opacity: 1 !important
}
</style>
