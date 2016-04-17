var plot_points = {{params.plot_points}};
var update_delay = {{params.update_delay}};
var updateTimeoutID;
var ctx;
var chart;

var chartOptions = {
	bezierCurve: true,
	showTooltips: true,
	scaleShowHorizontalLines: true,
	scaleShowLabels: true,
	scaleType: "date",
	scaleLabel: "\n<%=value%>°C",
	useUtc:false,
	animation:false
};

$(document).ready(function(){
	ctx = document.getElementById('{{params.name}}').getContext("2d");
	startUp();
});

function startUp(){
	update();
}

function update(){
	$.ajax({
		type:'GET',
		url:'temperature/' + plot_points,
		dataType:'json',
		success: function(resp){
			data = makeData(resp);
			chart = new Chart(ctx).Scatter(data,chartOptions);
		}
	});
	updateTimeoutID = setTimeout(update,update_delay);
}

function makeData(resp){
	console.log(resp);
	var data = []
	var points = []
	for(var i=0;i<resp.length;i++){
		point = {
			x:new Date(resp[i][0]),
			y:resp[i][1]
		};
		points.push(point);
	}
	var set = {
		strokeColor:"#A31515",
		data:points
	};
	data.push(set);
	return data;
}
