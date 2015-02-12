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
                },
                error: function(jqXHR, exception){
                	//alert("error");
                	//alert(jqXHR.responseText);
                	$("#alertdiv").html(
                		"<div class='alert alert-danger'>"+
						   "<a class='close' data-dismiss='alert' href='#' aria-hidden='true'>&times;</a>"+
						   "<strong>Error!</strong>  "+jqXHR.responseText+
						"</div>"
                	);
            	}
            	
            });
			
            /*$("#"+id).remove();
            $('#' + box).append('<center><div id="' + id + '">' + toy + '</div></center>');
            $('div#' + id).draggable({
                        helper: 'clone'
            });
            $(this).css('min-height' , 'auto');*/
        }
    });
 
});