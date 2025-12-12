////JQuery

//$.ajaxSetup({
//    async: false
//});

$(document).ready(function()
{

    // Adding new filter. Populate field-specific prompts.
    $("#filter_select").on('click', function() {

        //Clear out previous value stuff
        $("#filter_value_panel").empty();
        if ($(this).val() == "videoName")
        {
            $("#filter_value_panel").append("Enter name keywords:&nbsp <input type='text' id='videoName_input' name='videoName_input'>");
        }
        else if ($(this).val() == "description"){
            $("#filter_value_panel").append("Enter description keywords:&nbsp <input type='text' id='description_input' name='description_input'>");
        };
        $("#filter_value_panel").append("<input type='submit' id='add_filter' name='add_filter' value='Add Filter'>");

    });

// Being handled server-side
//    //Since this is added dynamically we need to catch event using a static object (e.g., document)
//    $(document).on('click', '#add_filter', function() {
//
//        $("#filter_div").append("<br><b>BUTTS</b>");
//    });

    //Remove selected filter item when x clicked
    $(".x_filter_button").click( function(){

        //alert($(this).attr("name"));

        //Remote the span for this filter
        $("#"+$(this).attr("name")+"_selected").remove();

        $("#videos_form").submit();

    });

    $("#add_video_button").click(function(){
        $("#new_video_div").css("visibility", "visible");
    });



});
