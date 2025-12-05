////JQuery

//$.ajaxSetup({
//    async: false
//});

$(document).ready(function()
{
    var submitButton = null;

    $("#filter_select").on('click', function() {

        //Clear out previous value stuff
        $("#filter_value_panel").empty();
        if ($(this).val() == "videoName")
        {
            $("#filter_value_panel").append("Enter name:&nbsp <input type='text' id='videoName_input'>");
        };
        $("#filter_value_panel").append("<input type='button' id='add_filter' name='add_filter' value='Add Filter'>");

    });

    //Since this is added dynamically we need to catch event using a static object (e.g., document)
    $(document).on('click', '#add_filter', function() {

        $("#filter_div").append("<br><b>BUTTS</b>");
    });



});
