$(document).ready(function(){
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
});

$(document).ready(function(){
	$("#form").submit(function(){
        $.ajax({
            type: "post",
            dataType: "json",
            data : {
            	'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
            	'content' : $("#content").val(),
            	'pk' : $("#pk").val()
            },
            url: "/tasks/mstnscmt/",
            success: function(data){
            var json = JSON.stringify(data);
                alert(json);
                $("#rez").html(json);
            },
            error: function(){
                alert("error");
            }
        });
        return false;
    });
});