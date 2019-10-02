gostApp.controller('ModalInstanceCtrl', function($uibModalInstance, $scope, $http, params) {

    $scope.data = params;
    $scope.data.steps = 20;
    $scope.data.combs = 100;
    $scope.data.m_rep = 0.5;
    $scope.data.c_ref = 1;

    /*$scope.selected = {
      item: $scope.data.patternType
    };*/

    $scope.ok = function () {
      $uibModalInstance.close();
    };
  
    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };

    /*$scope.runAcoGraank = function(data) {
        //var res = $http.post(getUrl() + '/v1.0/Things', newThing);
        var res = $http.post(getUrl() + "/py1.0", data);
        res.success(function(data, status, headers, config) {
            //alert( "added: " + JSON.stringify({data: data}));
          $scope.imgData = data
          msg = "+ : increasing and - : decreasing and x : irrelevant";
          $scope.info_msg = msg;
        });
        res.error(function(data, status, headers, config) {
            var msg = "failure: " + JSON.stringify({data: data});
            alert(msg);
            $scope.info_msg = msg;
        });
    };*/

  });