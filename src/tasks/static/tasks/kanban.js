$(document).ready(function() {
 
    $('.box .shadow').draggable({
        helper: 'clone'    
    });
     
    $('.box').droppable({
        tolerance: 'fit',
        drop: function(event,ui) {
            var id = $(ui.draggable).attr('id');
            var toy = $(ui.draggable).html();
            var box = $(this).attr('id');
			
			$.ajax({
                url: '/kanban/',
                type: 'GET',
                data: {
                    'id' : id,
                    'box' : box
                },
                success: function(data) {
                
                	var color = data['message'];
                	var user = data['explaination'];
                	
                    $("#"+id).remove();
		            $('#' + box).append('<div style="border-left: 6pt solid '+color+'" class="shadow" id="' + id + '">' + toy + '</div>');
		            $("#user"+id).html('<span class="glyphicon glyphicon-user"></span> ' + user);
		            $('div#' + id).draggable({
		            	helper: 'clone'
		            });
		            $(this).css('min-height' , 'auto');
		            
		            if(data['created'] == 'true'){
						preparecloseaction(data,"Resolve closed task",id);
						$('#myModal').modal('show');
		            }
		            
                },
                error: function(jqXHR, exception){
                	$("#alertdiv").html(
                		"<div class='alert alert-danger'>"+
						   "<a class='close' data-dismiss='alert' href='#' aria-hidden='true'>&times;</a>"+
						   "<strong>Error!</strong>  "+jqXHR.responseText+
						"</div>"
                	);
            	}
            	
            });
        }
    });
 
});

function preparecloseaction(data,graphtitle,id){
	$('#myModalLabel').text(graphtitle);
	//$('#content').text(data);
	
	// Get context with jQuery - using jQuery's .get() method.
	$("#content").html("");
	//mora da se obrise tag i opet doda, da bi se obrisala vrednost
	//posto recikliram grafik
	$("#content").html("<ul class=\"list-group\" id=\"closeid\" height=\"450\" width=\"600\" ></ul>");
	
	$.each(data['closedlist'], function(key, value) {
		//alert(key + ' ' + value);
		var address = "/resolve/".concat(key);
		address+="/";
		$( "#closeid" ).append("<li class='list-group-item'><a href='#' class='resolveclose' id='"+key+"' name='"+id+"'>"+ value +"</a></li>");
	});
}

$(document).delegate('a.resolveclose', 'click', function() { 
	//alert("BLAH");
	
	var resolveid = $(this).attr("id");
	var taskid = $(this).attr("name");
	
	//alert(resolveid+" "+taskid);
	
	$.ajax({
		url: '/resolve/',
		type: 'GET',
		data: {
			'resolveid' : resolveid,
			'taskid' : taskid
		},
		success: function(data) {
			//alert("OK");
		},
		error: function(jqXHR, exception){
			alert(jqXHR.responseText);
		}
	});
	

	$('#myModal').modal('hide');
});


