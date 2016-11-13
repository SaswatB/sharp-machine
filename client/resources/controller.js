//controller for page. 

function data_parser(callback){
		var x = document.getElementById("myFile");
		var f = new FileReader();
		var s;
		f.onload = function(){
			s = f.result;
			var bigArr = s.split('\n');
			for (i=0; i < bigArr.length; i++){
				console.log(bigArr[i]);
			}

			var j;
			var arr2 = new Array(bigArr.length);
			for(j=0; j<arr2.length; j++){
				arr2[j] = bigArr[j].split(',');
			}
      callback(arr2); 
      
		};
		f.readAsBinaryString(x.files[0]);
}

var app = angular.module('sm', []); 
app.controller('smCtrl', function($scope){
  $scope.pageIndex = 1; 
  $scope.file = null; 
  $scope.algorithms = []; 
  
  var socket = io(string = "http://1ee768f2.ngrok.io"); 
  socket.on('connect', function(){
    console.log("connected"); 
  });
  socket.on('init', function(data){
    console.log(data);
    $scope.algorithms = data; 
  }); 
  
  socket.on('disconnect', function(){console.log("disconnected");});  
  
  $scope.fileChanged = function(){
    data_parser(function(data){
      socket.emit("data", data);
    }); 
     
  }; 
  
  
  
  
  
}); 

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}