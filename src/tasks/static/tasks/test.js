/*$(document).ready(function(){
    $("#comment").click(function(){
        $.ajax({
            type: "GET",
            url: "/tasks/mstnscmt/",
            success: function(data){
            var json = JSON.stringify(data);
                alert(json);
            },
            error: function(){
                alert("error");
            }
        });
    });
});*/

$(document).ready(function(){
	$("#form").submit(function(){
        $.ajax({
            type: "post",
            dataType: "json",
            data : {
            	'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
            	'content' : $("#ccontent").val(),
            	'pk' : $("#pk").val()
            },
            url: "/tasks/mcomment/",
            
            success: function(data){
            
                var content = data['content'];
                var usr = data['user'];
                var dt = data['date'];
                
            	$("#rez").append("<li class=\"list-group-item\"><div>"+ content +" "+ usr +" "+ dt +"</div></li>");
            	 $("#ccontent").val("")
            },
            
            error: function(){
                alert("error");
            }
        });
        return false;
    });
});

$(document).ready(function() {
    $('#datepicker').datepicker();
});