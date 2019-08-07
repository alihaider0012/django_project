$(document).ready(function(){
    $('#logout_link').click(function(){
        $('#logout_form').submit();
    });

    $('#nav_search_button').click(function(){
        if($('#navsearch').val()=='')
        {
            return;
        }
        $(this).closest('form').submit()
    });
    
    
});
