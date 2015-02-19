
$(function() {

	var barOptions = {
	        scaleIntegersOnly: false,
	        //barValueSpacing : 0.5,
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
	
	var lineOptions = {
	        legendTemplate : '<ul class=\"<%=name.toLowerCase()%>-legend\">'
	        	+'<% for (var i=0; i<datasets.length; i++){%>'
	        	+'<li>'
	        	+'<span style=\"background-color:<%=datasets[i].strokeColor%>\"></span>'
	        	+'<%if(datasets[i].label){%><%=datasets[i].label%><%}%>'
	        	+'</li>'
	        	+'<%}%>'
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
	                color:"#00D965",
	                highlight: "#00E56A",
	                label: "Closed"
	            }
	        ]
	
	var barData = {
			labels: bar_labels,
	        datasets: [				
				{
				    label: "Tasks",
				    fillColor : "rgba(0,217,101,0.2)",
					strokeColor : "rgba(0,217,101,0.8)",
					pointColor : "rgba(0,217,101,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(0,217,101,0.2)",
				    data: hours
				}
			]
	};
	
	var lineData = {
			 labels: date_labels,
	         datasets: [	
				{
				    label: "Created",
				    fillColor : "rgba(255,249,116,0.5)",
					strokeColor : "rgba(255,249,116,0.8)",
					pointColor : "rgba(255,249,116,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(255,249,116,0.2)",
				    data: created
				},
				{
				    label: "On Wait",
				    fillColor : "rgba(122,229,232,0.5)",
					strokeColor : "rgba(122,229,232,0.8)",
					pointColor : "rgba(122,229,232,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(122,229,232,0.2)",
				    data: onwait
				},
				{
				    label: "In progress",
				    fillColor : "rgba(255,111,99,0.5)",
					strokeColor : "rgba(255,111,99,0.8)",
					pointColor : "rgba(255,111,99,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(111,23,21,0.2)",
				    data: in_progress
				},
				{
				    label: "Done",
				    fillColor : "rgba(0,217,101,0.5)",
					strokeColor : "rgba(0,217,101,0.8)",
					pointColor : "rgba(0,217,101,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(0,217,101,0.2)",
				    data: done
				}
			]
	};
	
	var ctx1 = $("#myChart1").get(0).getContext("2d");
    var myPieChart;
    
	var ctx2 = $("#myChart2").get(0).getContext("2d");
	var myBarChart;
	
	var ctx3 = $("#myChart3").get(0).getContext("2d");
	var myLineChart;

    $('#tab2').on('shown.bs.tab', function (e) {
        myPieChart = new Chart(ctx1).Pie(pieData,pieOptions);
       
        var legend1 = myPieChart.generateLegend();
        $("#legend1").html(legend1);
    });
    
	$('#tab3').on('shown.bs.tab', function (e) {
		myBarChart = new Chart(ctx2).Bar(barData, barOptions);
		
		 var legend = myBarChart.generateLegend();
	     $("#legend2").html(legend);
	});    
  
    $('#tab4').on('shown.bs.tab', function (e) {
		myLineChart = new Chart(ctx3).Line(lineData, lineOptions);
		
		var legend = myLineChart.generateLegend();
	    $("#legend3").html(legend);
	}); 
	   
});