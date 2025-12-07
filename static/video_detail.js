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




});