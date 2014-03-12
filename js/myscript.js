$(document).ready(function(){
    $('select#sort').change(function(){
        switch ($(this).val()) {
            case "datetime": $.cookie("sort","datetime"); break;
            case "datetime_reverse": $.cookie("sort","datetime_reverse"); break;
            case "filedate": $.cookie("sort","filedate"); break;
            case "filedate_reverse": $.cookie("sort","filedate_reverse"); break;
            default : $.cookie("sort","unknown");
        }
        location.reload();
    });
    $(".grid a").colorbox({width:"80%",height:"80%"});
});
