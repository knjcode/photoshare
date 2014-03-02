$(document).ready(function(){
    $('select#sort').change(function(){
        switch ($(this).val()) {
            case "datetime": $.cookie("sort","datetime"); $('p').text($.cookie("sort")); break;
            case "datetime_reverse": $.cookie("sort","datetime_reverse"); $('p').text($.cookie("sort")); break;
            case "filedate": $.cookie("sort","filedate"); $('p').text($.cookie("sort")); break;
            case "filedate_reverse": $.cookie("sort","filedate_reverse"); $('p').text($.cookie("sort")); break;
            default : $.cookie("sort","unknown");
        }
    });
});
