// Things controller
gostApp.controller('ThingsCtrl', function ($scope, $http, $uibModal) {
    $scope.Page.setTitle('THINGS');
    $scope.Page.setHeaderIcon(iconThing);

    $http.get(getUrl() + "/v1.0/Things").then(function (response) {
        $scope.thingsList = response.data.value;
    });

    $scope.thingClicked = function (thingID) {
        angular.forEach($scope.things, function (value, key) {
            if (value["@iot.id"] == thingID) {
                $scope.Page.selectedThing = value;
            }
        });

        $scope.Page.go("thing/" + thingID);
    };

    $scope.addNewThing = function(newThing) {
        var res = $http.post(getUrl() + '/v1.0/Things', newThing);
        res.success(function(data, status, headers, config) {
            alert( "added: " + JSON.stringify({data: data}));
        });
        res.error(function(data, status, headers, config) {
            alert( "failure: " + JSON.stringify({data: data}));
        });
    };

    $scope.deleteThingClicked = function (entity) {
        var res = $http.delete(getUrl() + '/v1.0/Things(' + entity["@iot.id"] + ')');
        res.success(function(data, status, headers, config) {
            var index = $scope.thingsList.indexOf(entity);
            $scope.thingsList.splice(index, 1);
        });
        res.error(function(data, status, headers, config) {
            alert( "failure: " + JSON.stringify({data: data}));
        });
     };

    $scope.initAddThing = function(){
        console.log("starting dialog for new thing")
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'addNewThingContent.html',
            controller: 'NewThingInstanceCtrl'
          });

        modalInstance.result.then(function(thing){   
            addNewThing(thing);
        });
    }

});

gostApp.controller('NewThingInstanceCtrl', function($uibModalInstance, $scope) {
    
    $scope.newThing = {};

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };

    $scope.addThing = function(){
        $uibModalInstance.close($scope.newThing);
    };

  });