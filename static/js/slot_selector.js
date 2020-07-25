let slots = [];

function removeA(arr) {
    var what, a = arguments, L = a.length, ax;
    while (L > 1 && arr.length) {
        what = a[--L];
        while ((ax = arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1);
        }
    }
    return arr;
}

function changeMyPosition(slot_id) {
    let selected_slot = document.getElementById(slot_id);
    // console.log(document.getElementById('all_choices').contains(selected_slot));
    if (document.getElementById('all_choices').contains(selected_slot)) {
        console.log('Hello 1');
        document.getElementById('all_choices').removeChild(selected_slot);
        document.getElementById('selected_choices').appendChild(selected_slot);
        slots.push(slot_id);
    }
    else if (document.getElementById('selected_choices').hasChildNodes(selected_slot)) {
        console.log('Hello 2');
        document.getElementById('selected_choices').removeChild(selected_slot);
        document.getElementById('all_choices').appendChild(selected_slot);
        removeA(slots, slot_id);
    }
    console.log(slots);
}

function addHiddenInputTags() {
    if (slots.length != 4) {
        alert('You have to select 3 preferences');
    }
    else {
        let my_form = document.getElementById('my_form');
        let obj1 = document.createElement('input')
        obj1.name = 'preference1'
        obj1.type = 'text';
        obj1.value = slots[0];
        my_form.appendChild(obj1);

        let obj2 = document.createElement('input')
        obj2.name = 'preference2'
        obj2.type = 'text';
        obj2.value = slots[1];
        my_form.appendChild(obj2);

        let obj3 = document.createElement('input')
        obj3.name = 'preference3'
        obj3.type = 'text';
        obj3.value = slots[2];
        my_form.appendChild(obj3);

        let obj4 = document.createElement('input')
        obj4.name = 'preference4'
        obj4.type = 'text';
        obj4.value = slots[3];
        my_form.appendChild(obj4);

        document.getElementById('submit_choice').click();
    }

}