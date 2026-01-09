////JQuery

//$.ajaxSetup({
//    async: false
//});

$(document).ready(function()
{
    $("#edit_detail_button").click(function(){
        $(this).prop("disabled",true);
        $("#id_input").prop("readonly",true);
        $("#tag_input").prop("readonly",true);
        $("#save_detail_input").css("visibility", "visible");
        $("#tag_select_span").css("visibility", "visible");
        $("#add_tag_button").css("visibility", "visible");
        $("#location_select_span").css("visibility", "visible");
        //Don't seem to need .each() fun
//        $(".detail_value_field").each(function(){
//            $(this).prop("disabled",false);
//        });
        $(".detail_value_field").prop("disabled",false);
        $(".x_filter_button").css("visibility", "visible");

    });

    $("#edit_thumbnail_button").click(function(){
        $("#edit_thumbnail_button").prop("disabled", true);
        $("#thumbnail_div").append("<span> Seconds in:&nbsp <input type='text' id='thumbnail_input' name= 'thumbnail_input'> <input type='submit' name='thumbnail_submit' value='Save'> </span>");

    });

    $("#delete_video_button").click(function(){
        $("#delete_confirm").css("visibility","visible");
    });

    $("#add_tag_button").click(function(){
        $(location).attr('href', "video_tags");
    });

    $("#tag_select").on('change', function() {
        //////Old way of concatentating text field with tags (LAME)
//        var current_tags = $("#tag_input").val();
//        if (current_tags == "None"){
//            $("#tag_input").val($(this).val());
//        }
//        else{
//            $("#tag_input").val( current_tags + " " +$(this).val());
//        }
        /////////////////
        var tag = $(this).val();

        //Remove selected tag from select
        $(this).find("[value='"+tag+"']").remove();

        //Append tag box
        var tag_button =
            "<span id='"+tag+"_selected'>" +
            "   <span class='selected_filter'>" +
            "       <input class='selected_filter_value' type='text' readonly name='"+tag+"_tag_input' value='"+tag+"'>&nbsp <img class='x_filter_button' name='"+tag+"' src='static/x.png'/>&nbsp " +
            "   </span> &nbsp" +
            "</span>"
            ;
        $("#tags_span").append(tag_button);

    });

    $("#location_select").on('change', function() {
        $("#location_input").val($(this).val());
    });


//    $(".x_filter_button").click( function(){
    $(document).on('click', '.x_filter_button', function() {

        //alert($(this).attr("name"));

        var tag_name = $(this).attr("name");

        //Remote the span for this filter
        $("#"+tag_name+"_selected").remove();

        //Add removed tag back to select
        var tag_select = $('#tag_select');
        tag_select.append("<option value='"+tag_name+"'>"+tag_name+"</option>");

        //Get all tag options and re-sort
        var tags = tag_select.children('option');
        tags.sort(function(a, b) {
            var compA = $(a).text().toUpperCase();
            var compB = $(b).text().toUpperCase();
            return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
        });

        //tag_select.clear();
        $.each(tags, function(idx, itm) {
            tag_select.append(itm);

            //debug
            //$("#video_detail").append("<br>"+$(itm).val());
        });
    });

});