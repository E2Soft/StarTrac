/*$(document).ready(function(){
    $("#comment").click(function(){
        $.ajax({
            type: "GET",
            url: "/mstnscmt/",
            success: function(data){
            var json = JSON.stringify(data);
                //alert(json);
            },
            error: function(){
                //alert("error");
            }
        });
    });
});*/

$(document).ready(function() {
    $('#datepicker').datepicker();
});

$(document).ready(function() {
    $('#addtask').click(function(){
        //alert("TREBA DODATI LINK!");
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
            url: $("#comment_ajax_url").val(),
            
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
                //alert("error");
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
            dataType: "json",
            data : {
            	'pk' : $("#pk").val()
            },
            url: reversed_urls.graph,
            success: function(data){
            var json = JSON.stringify(data);
                //alert(json);
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
            dataType: "json",
            data : {
            	'pk' : $("#pk").val()
            },
            url: reversed_urls.prioritygraph,
            success: function(data){
            var json = JSON.stringify(data);
                //alert(json);
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
            url: reversed_urls.resolvegraph,
            success: function(data){
            var json = JSON.stringify(data);
                //alert(json);
                preparegraph(data,"Tasks resolved graph");
                $('#myModal').modal('show');
            },
            error: function(){
                alert("error");
            }
        });
    });
});

$(document).ready(function(){
    $("#reqgraph").click(function(){
        $.ajax({
            type: "GET",
            dataType: "json",
            data : {
            	'pk' : $("#pk").val()
            },
            url: reversed_urls.reqgraph,
            success: function(data){
            var json = JSON.stringify(data);
                //alert(json);
                preparegraph(data,"Requirement tasks states graph");
                $('#myModal').modal('show');
            },
            error: function(){
                alert("error");
            }
        });
    });
});

$(document).ready(function(){
    $("#reqpriority").click(function(){
        $.ajax({
            type: "GET",
            dataType: "json",
            data : {
            	'pk' : $("#pk").val()
            },
            url: reversed_urls.reqprioritygraph,
            success: function(data){
            var json = JSON.stringify(data);
                //alert(json);
                preparegraph(data,"Requirement priority graph");
                $('#myModal').modal('show');
            },
            error: function(){
                alert("error");
            }
        });
    });
});

$(document).ready(function(){
    $("#reqresolve").click(function(){
        $.ajax({
            type: "GET",
            dataType: "json",
            data : {
            	'pk' : $("#pk").val()
            },
            url: reversed_urls.reqresolvegraph,
            success: function(data){
            var json = JSON.stringify(data);
                //alert(json);
                preparegraph(data,"Requirement resolve graph");
                $('#myModal').modal('show');
            },
            error: function(){
                alert("error");
            }
        });
    });
});

jQuery(document).ready(function($) {
      $(".clickableRow").click(function() {
      		
      		var x = $(this).offset().left;
  			var y = $(this).offset().top;
  			var target = $(this);
      		
            $.ajax({
            type: "GET",
            dataType: "json",
            data : {
            	'pk' : $(this).attr('id')
            },
            url: reversed_urls.eventinfo,
            success: function(data){
            	var json = JSON.stringify(data);
                //alert(json);
                
                $( "#dialog-3" ).html("<ul class=\"list-group\" id=\"jumps\"></ul>");
                for(var i = 0; i < data.length; i++) {
				    $( "#jumps" ).append("<li class='list-group-item'><a href='"+ data[i].url +"'>"+"<span class='"+ data[i].glyph +"'></span> "+data[i].name+"</a></li>");
				}
                
                $(function() {
		            $( "#dialog-3" ).dialog({
		               autoOpen: false, 
		               hide: "puff",
		               show : "slide",
		               position: {my: 'bottom', at: 'bottom', of: target},
		               modal : true,
		               draggable: false,
		               title : "Choose where to go"
		            });

		            $( "#dialog-3" ).dialog( "open" );
		         });
                
            },
            error: function(){
                alert("error");
            }
        });
      });
});

$(document).ready(function() {
	$('#colorpickerfield').colorpicker();
});










