gostApp.controller('ModalInstanceCtrl', function($uibModalInstance, $scope, $http, params) {
  
    $scope.reps = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];

    $scope.data = params;
    $scope.data.steps = 20;
    $scope.data.combs = 100;
    $scope.data.m_rep = 0.5;
    $scope.data.c_ref = 0;

    $scope.repClicked = function(sel_rep){
        $scope.data.m_rep = sel_rep;
    }

    $scope.refClicked = function(sel_ref){
        $scope.data.c_ref = sel_ref;
    }
  
    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };

    $scope.runAcoGraank = function(){
        $uibModalInstance.close($scope.data);
    };
  });