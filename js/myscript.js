$(function(){
    $('a img').hover(function(){
        $(this).fadeTo("normal",0.6);
    },function(){
        $(this).fadeTo("normal",1.0);
    });
});