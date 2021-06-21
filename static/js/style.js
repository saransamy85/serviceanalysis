$(function(){
    $('#analysisbtn').click(function(){
        $('.analysiscont').css("display","inline");
        $('.homecont').css("display","none");
        

    });
    $('#homebtn').click(function(){
        $('.homecont').css("display","inline");
        $('.analysiscont').css("display","none");
        
    });
    $('#menubar').click(function(){
        if($('#sidemenu').css('display')=='none')
        {
            $('#sidemenu').css("display","block");
        }
        else
        {
            $('#sidemenu').css("display","none");
        }
        
    });
});
