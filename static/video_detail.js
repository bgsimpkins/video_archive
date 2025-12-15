////JQuery

//$.ajaxSetup({
//    async: false
//});

$(document).ready(function()
{
    $("#edit_detail_button").click(function(){
        $(this).prop("disabled",true);
        $("#save_detail_input").css("visibility", "visible");
        $(".detail_value_field").each(function(){
            $(this).prop("disabled",false);
        });
    });

    $("#edit_thumbnail_button").click(function(){
        $("#edit_thumbnail_button").prop("disabled", true);
        $("#thumbnail_div").append("<span> Seconds in:&nbsp <input type='text' id='thumbnail_input' name= 'thumbnail_input'> <input type='submit' name='thumbnail_submit' value='Save'> </span>");

    });

    $("#delete_video_button").click(function(){
        $("#delete_confirm").css("visibility","visible");
    });
});