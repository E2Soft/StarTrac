
$(function() {

	var barOptions = {
	        scaleIntegersOnly: false,
	        barValueSpacing : 0.5,
	        legendTemplate : '<ul class=\"<%=name.toLowerCase()%>-legend\">'
	        	+'<% for (var i=0; i<datasets.length; i++){%>'
	        	+'<li>'
	        	+'<span style=\"background-color:<%=datasets[i].strokeColor%>\"></span>'
	        	+'<%if(datasets[i].label){%><%=datasets[i].label%><%}%>'
	        	+'</li>'
	        	+'<%}%>'
	        	+'</ul>'	        	
	};
	
	var pieOptions = {
			legendTemplate : '<ul class=\"<%=name.toLowerCase()%>-legend\">'
                +'<% for (var i=0; i<segments.length; i++) { %>'
                +'<li>'
                +'<span style=\"background-color:<%=segments[i].fillColor%>\"></span>'
                +'<% if (segments[i].label) { %><%= segments[i].label %><% } %>'
                +'</li>'
                +'<% } %>'
                +'</ul>'       	
	};
	
	var pieData = [
	            {
	                value: created_tasks,
	                color:"#FFF974",
	                highlight: "#FFF99C",
	                label: "Created"
	            },
	            {
	                value: onwait_tasks,
	                color: "#7ADCE8",
	                highlight: "#AADCE8",
	                label: "OnWait"
	            },
	            {
	                value: accepted_tasks,
	                color:"#FF6F63",
	                highlight: "#FF8263",
	                label: "Accepted"
	            },
	            {
	                value: closed_tasks,
	                color:"#6FF272",
	                highlight: "#6FF28D",
	                label: "Closed"
	            }
	        ]
	
	var barData = {
			labels: bar_labels,
	        datasets: [				
				{
				    label: "Tasks",
				    fillColor : "rgba(220,220,220,0.2)",
					strokeColor : "rgba(220,220,220,1)",
					pointColor : "rgba(220,220,220,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(220,220,220,1)",
				    data: hours
				}
			]
	};
	
	var ctx1 = $("#myChart1").get(0).getContext("2d");
    var myPieChart;
    
	var ctx2 = $("#myChart2").get(0).getContext("2d");
	var myBarChart;
	    
	$('#tab3').on('shown.bs.tab', function (e) {
		myBarChart = new Chart(ctx2).Bar(barData, barOptions);
		
		 var legend = myBarChart.generateLegend();
	     $("#legend2").html(legend);
	});    

    $('#tab2').on('shown.bs.tab', function (e) {
        myPieChart = new Chart(ctx1).Pie(pieData,pieOptions);
       
        var legend1 = myPieChart.generateLegend();
        $("#legend1").html(legend1);
    });
	   
});