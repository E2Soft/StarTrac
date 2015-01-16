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

$(document).ready(function(){
	$("#formreq").submit(function(){
        $.ajax({
            type: "post",
            dataType: "json",
            data : {
            	'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
            	'content' : $("#ccontent").val(),
            	'pk' : $("#pk").val()
            },
            url: "/tasks/rcomment/",
            
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
    $("#ccontent").keyup(function(){
    	if($("#ccontent").val().length > 0){
    		$("#err").attr("class","form-group");
    		$("#btncomment").attr("class","btn btn-warning");
    	}else{
    		$("#err").attr("class","form-group has-error has-feedback");
    		$("#btncomment").attr("class","btn btn-warning disabled");
    	}
  	});
});


function preparegraph(data,graphtitle){
	$('#myModalLabel').text(graphtitle);
	//$('#content').text(data);
	
	// Get context with jQuery - using jQuery's .get() method.
	$("#content").html("");
	//mora da se obrise tag i opet doda, da bi se obrisala vrednost
	//posto recikliram grafik
	$("#content").html("<canvas id=\"canvas\" height=\"450\" width=\"600\"></canvas>");
	
	var ctx = $("#canvas").get(0).getContext("2d");
	
	// This will get the first returned node in the jQuery collection.
	var myNewChart = new Chart(ctx);
	
	var myPieChart = new Chart(ctx).Pie(data);
}

$(document).ready(function(){
    $("#graph").click(function(){
        $.ajax({
            type: "GET",
            url: "/tasks/graph/",
            success: function(data){
            var json = JSON.stringify(data);
                alert(json);
                preparegraph(data,"Tasks states graph");
                $('#myModal').modal('show');
            },
            error: function(){
                alert("error");
            }
        });
    });
});

$(document).ready(function(){
    $("#priority").click(function(){
        $.ajax({
            type: "GET",
            url: "/tasks/prioritygraph/",
            success: function(data){
            var json = JSON.stringify(data);
                alert(json);
                preparegraph(data,"Tasks priority graph");
                $('#myModal').modal('show');
            },
            error: function(){
                alert("error");
            }
        });
    });
});

$(document).ready(function(){
    $("#resolve").click(function(){
        $.ajax({
            type: "GET",
            dataType: "json",
            data : {
            	'pk' : $("#pk").val()
            },
            url: "/tasks/resolvegraph/",
            success: function(data){
            var json = JSON.stringify(data);
                alert(json);
                preparegraph(data,"Tasks resolved graph");
                $('#myModal').modal('show');
            },
            error: function(){
                alert("error");
            }
        });
    });
});


















