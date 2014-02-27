$(document).ready(function(){
    $('a img').hover(
        function(){
            $(this).fadeTo("fast",0.6);
        },
        function(){
            $(this).fadeTo("fast",1.0);
        }
    );
    $('p').text($.cookie("sort"));

    sort = $("#sort");
    $('#sort').bind('change',function(){
        switch (sort.val()) {
            case "datetime": $.cookie("sort","datetime"); $('p').text($.cookie("sort")); break;
            case "datetime_reverse": $.cookie("sort","datetime_reverse"); $('p').text($.cookie("sort")); break;
            case "filedate": $.cookie("sort","filedate"); $('p').text($.cookie("sort")); break;
            case "filedate_reverse": $.cookie("sort","filedate_reverse"); $('p').text($.cookie("sort")); break;
            default : $.cookie("sort","unknown");
        }
    });

});