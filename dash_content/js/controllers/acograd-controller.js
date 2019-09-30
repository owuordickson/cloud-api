gostApp.controller('AcoGradCtrl', function ($scope, $http) {
    $scope.Page.setTitle('GRADUAL PATTERNS');
    $scope.Page.setHeaderIcon(iconAcograd);
    
    /*$http.post(getPysocketUrl()).then(function (response) {
        $scope.Pymsg = response;
        $scope.Pyurl = getPysocketUrl();
    });

    $http.get(getUrl() + "/v1.0/Datastreams").then(function (response) {
        $scope.Gomsg = response;
        $scope.datastreamsList = response.data.value;
        $scope.Gourl = getUrl();
    });*/

    var res = $http.get(getUrl() + "/py1.0");
    res.success(function(data, status, headers, config) {
        //alert( "added: " + JSON.stringify({data: data}));
        $scope.Pymsg = data;//JSON.stringify({data: data});
        $scope.Pyurl = status;
    });
    res.error(function(data, status, headers, config) {
        $scope.Pymsg = JSON.stringify({data: config});
        $scope.Pyurl = status;
        //alert( "failure: " + JSON.stringify({data: data}));
    });
    
    $scope.runAcoGraank = function(dataStreams) {
        //var res = $http.post(getUrl() + '/v1.0/Things', newThing);
        var res = $http.post(getPysocketUrl(), dataStreams);
        res.success(function(data, status, headers, config) {
            //alert( "added: " + JSON.stringify({data: data}));
           $scope.imgData = data
        });
        res.error(function(data, status, headers, config) {
            alert( "failure: " + JSON.stringify({data: data}));
        });
    };

    /*$scope.datastreamClicked = function (datastreamID) {
        angular.forEach($scope.things, function (value, key) {
            if (value["@iot.id"] == thingID) {
                $scope.Page.selectedDatastream = value;
            }
        });

        $scope.Page.go("datastream/" + datastreamID);
    };

     $scope.deleteDatastreamClicked = function (entity) {
        var res = $http.delete(getUrl() + '/v1.0/Datastreams(' + entity["@iot.id"] + ')');
        res.success(function(data, status, headers, config) {
            var index = $scope.datastreamsList.indexOf(entity);
            $scope.datastreamsList.splice(index, 1);
        });
        res.error(function(data, status, headers, config) {
            alert( "failure: " + JSON.stringify({data: data}));
        });
     };*/
});