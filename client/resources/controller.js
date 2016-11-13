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
        var arr2 = [];
        for(j=0; j<bigArr.length; j++){
            if(bigArr[j].trim().length == 0){
                break;
            }
            var temp = bigArr[j].split(',');
            var arr3 = new Array(temp.length);
            for(i=0; i<temp.length; i++){
                arr3[i] = parseInt(temp[i]);
            }
            arr2.push(arr3);
        }
        callback(arr2); 
    };
    f.readAsBinaryString(x.files[0]);
}

var app = angular.module('sm', []); 
app.controller('smCtrl', function($scope){
    $scope.pageIndex = 1; 
    $scope.file = null; 
    $scope.algorithms = [{"name": 4}]; 
    $scope.algoChoice = -1;
    $scope.trainingData = null;
    
    var socket = io(string = "http://70f511dd.ngrok.io"); 
    socket.on('connect', function(){
        console.log("connected"); 
    });
    socket.on('init', function(data){
        console.log(data);
        $scope.algorithms = data; 
        $scope.$apply();
        console.log(data);
    }); 
      
    socket.on('disconnect', function(){console.log("disconnected");});  
      
    $scope.fileChanged = function(){
        data_parser(function(data){
            $scope.trainingData = data;
        }); 
    }; 
    $scope.train = function(){
        if(!$scope.trainingData || $scope.algoChoice==1){
            alert("Please enter all fields before continuing");
            return;
        }
        socket.emit("train", {"data": $scope.trainingData, "algorithm": $scope.algoChoice});
        $scope.pageIndex = 2; 
    }
    
}); 
