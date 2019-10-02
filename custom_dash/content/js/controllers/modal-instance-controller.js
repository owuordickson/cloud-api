gostApp.controller('ModalInstanceCtrl', function($uibModalInstance, $scope, $http, params) {

    $scope.data = params;
    $scope.data.steps = 20;
    $scope.data.combs = 100;
    $scope.data.m_rep = 0.5;
    $scope.data.c_ref = 1;

    /*$scope.selected = {
      item: $scope.data.patternType
    };

    $scope.ok = function () {
        $uibModalInstance.close();
    };*/
  
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };

    $scope.runAcoGraank = function(){
        $uibModalInstance.close($scope.data);
    };
  });