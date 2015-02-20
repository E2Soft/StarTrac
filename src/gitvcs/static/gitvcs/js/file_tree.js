$(document).ready(function()
{
	$('.file-tree').each(function() 
	{
		$( this ).children().css( "display", "none" );
		
		$( this ).fileTree(
		{
			data: JSON.parse($( this ).text()),
			sortable: false,
			selectable: false
		});
	});
});