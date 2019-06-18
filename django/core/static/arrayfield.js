if (!$) {
    $ = django.jQuery
}

function deleteTextInput(element) {
    let liElement = element.parentNode;
    let ulElement = liElement.parentNode;

    if ($('li', ulElement).length > 2) {
        ulElement.removeChild(liElement)
    }
    else {
        $(liElement).find('input').val('')
    }
}

function addNewInputElement(element) {
    let ulElement = element.parentNode;
    let liElement = $(ulElement.parentNode);

    let elementCounter = liElement.data('element-counter');
    elementCounter++;
    liElement.data('element-counter', elementCounter);

    let elementName = liElement.attr('id') + '_' + elementCounter;

    let clonedItem = liElement.children(":first").clone();
    clonedItem.find('input').attr('name', elementName).attr('id', 'id_'+elementName).val('');
    clonedItem.find('select').attr('name', elementName).attr('id', 'id_'+elementName);
    clonedItem.find('select option:first').attr('selected', true);
    clonedItem.insertBefore(liElement.find('li:last'))
}

$(document).on('click', '.add-arraywidget-item', function(e) {
    e.preventDefault();
    addNewInputElement(e.target)
});

$(document).on('click', '.delete-arraywidget-item', function(e) {
    e.preventDefault();
    deleteTextInput(e.target)
});

$(document).on("change", '#fields-group td.field-type select', function(e) {
    let parent = e.target.parentNode.parentNode;
    let list = $('.arrayfield-list', parent);
    let value = +e.target.value;

    if (value === 4 || value === 5 ) {
        list.show()
    }
    else {
        list.hide()
    }
});

$( document ).ready(function() {
    $('#fields-2-group .arrayfield-list').show()
});
