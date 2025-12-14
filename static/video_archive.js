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
        }
        else if ($(this).val() == "location"){
            $("#filter_value_panel").append("Enter location keywords:&nbsp <input type='text' id='location_input' name='location_input'>");
        }
        else if ($(this).val() == "tags"){
            $("#filter_value_panel").append("Enter tags keywords:&nbsp <input type='text' id='tags_input' name='tags_input'>");
        }
        else if ($(this).val() == "theDate"){
            $("#filter_value_panel").append("Enter date range:&nbsp <input type='text' id='date_start_input' name='date_start_input' value='1970-01-01' style='width:80px'> &nbsp to &nbsp <input type='text' id='date_end_input' name='date_end_input' value='9999-12-31' style='width:80px'>");
            //$("#filter_value_panel").append("Enter date range:&nbsp <input type='hidden' id='theDate_input' name='theDate_input' value='1970-01-01 to 9999-12-31'>");
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

        //Reuse 'add_filter' input (used above) so that offset is set back to 1 when form processed
        $("#filter_value_panel").append("<input type='hidden' id='add_filter' name='add_filter' value='Add Filter'>");
        $("#videos_form").submit();

    });

    $("#add_video_button").click(function(){
        $("#new_video_div").css("visibility", "visible");
    });

    $(".video_row").click(function(){
        //#alert("stuff!");
        var id =  $(this).find("#id").text();
        $(location).attr('href', "video_detail?id="+id);
    });

});
