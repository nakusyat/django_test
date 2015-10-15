$(document).ready(function(){
    $('input[type="radio"]').on('change', function() {
        $(this).closest("div").find("input").not(this).prop('checked', false);
    });

    $('input[type="number"]').on('change',function(){
        $(this).closest('li').find('input').not(this).prop('checked', true);
    });

    $('form[name="word_align"]').submit(function(){
        if( !$("input[name=source]").is(":checked") || !$("input[name=target]").is(":checked") )
        {
            alert('No source or target file is selected!');
            return false;
        }

    });
    $('.delete').on('click', function(){
        if (confirm('Do you want to delete?')) {
            return true;
        } else {
            return false;
        }
    });
});