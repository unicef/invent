(function() {

    if (!$) {
        $ = django.jQuery
    }

    function deleteTextInput(element) {
        var liElement = element.parentNode
        var ulElement = liElement.parentNode

        if ($('li', ulElement).length > 2) {
            ulElement.removeChild(liElement)
        }
        else {
            $(liElement).find('input').val('')
        }
    }

    function addNewInputElement(element) {
        var ulElement = element.parentNode
        var liElement = $(ulElement.parentNode)

        var elementCounter = liElement.data('element-counter')
        elementCounter++
        liElement.data('element-counter', elementCounter)

        var elementName = liElement.attr('id') + '_' + elementCounter

        var clonedItem = liElement.children(":first").clone()
        clonedItem.find('input').attr('name', elementName).attr('id', 'id_'+elementName).val('')
        clonedItem.find('select').attr('name', elementName).attr('id', 'id_'+elementName)
        clonedItem.find('select option:first').attr('selected', true)
        clonedItem.insertBefore(liElement.find('li:last'))
    }

    function showHideOptionsField(selector) {
        var showValues = [4, 5];
        var row = selector.closest('.form-row');
        var list = row.querySelector('.field-options .arrayfield-list');
        var value = parseInt(selector.value, 10);

        if (showValues.includes(value)) {
            list.style.display = 'block';
        } else {
            list.style.display = 'none'
        }
    }


    $(document).on('click', '.add-arraywidget-item', function(e) {
        e.preventDefault()
        addNewInputElement(e.target)
    })

    $(document).on('click', '.delete-arraywidget-item', function(e) {
        e.preventDefault()
        deleteTextInput(e.target)
    })

    $(document).on("change", '#fields-group .form-row td.field-type select', function(e) {
        showHideOptionsField(e.target);
    })

    $( document ).ready(function() {
        $('#fields-2-group .arrayfield-list').show()
        document.querySelectorAll('#fields-group .form-row.dynamic-fields td.field-type select')
            .forEach(showHideOptionsField)
    })
})()