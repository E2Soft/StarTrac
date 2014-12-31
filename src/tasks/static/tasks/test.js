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
                
                var contentlogo = "<span class=\"glyphicon glyphicon-comment\"></span>";
				var usrlogo = "<p><span class=\"glyphicon glyphicon-user\"></span>";
				var dtlogo = "<span class=\"glyphicon glyphicon-calendar\"></span>";
                
            	$("#rez").append("<li class=\"list-group-item\">"+ contentlogo+" "+content +" "+usrlogo+" "+usr+"</p>"+" "+dtlogo+" "+dt +"</li>");
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

$(document).ready(function() {
    $('#addtask').click(function(){
        alert("TREBA DODATI LINK!");
    });
});