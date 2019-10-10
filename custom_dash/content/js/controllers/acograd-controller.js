gostApp
.directive('loading', function () {
    return {
      restrict: 'E',
      replace:true,
      template: '<div class="loading"><img src="images/loading.gif" width="40" height="40" />  working...</div>',
      link: function (scope, element, attr) {
            scope.$watch('loading', function (val) {
                if (val)
                    $(element).show();
                else
                    $(element).hide();
            });
      }
    }
})
.directive('results', function () {
    return {
      restrict: 'E',
      replace:true,
      template: '<div class="results"><img src="images/Figure.png" width="420" height="400" /></div>',
      link: function (scope, element, attr) {
            scope.$watch('results', function (val) {
                if (val)
                    $(element).show();
                else
                    $(element).hide();
            });
      }
    }
})
.controller('AcoGradCtrl', function ($scope, $http, $uibModal, $q, $timeout) {
    $scope.Page.setTitle('GRADUAL PATTERNS');
    $scope.Page.setHeaderIcon(iconAcograd);

    //var $ctrl = this;
    $scope.info_title = "information";
    $scope.info_msg = "click 'execute' button to cross different datastreams";
    $scope.supports = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
    $scope.patterns = ["emerging","gradual"];

    $scope.newParams = {};
    $scope.newParams.minSup = 0.5;
    $scope.newParams.patternType = "gradual";
    $scope.newParams.crossingList = null;

    $scope.ds_model = [];
    $scope.ds_data = [];
    $scope.observationList = [];
    $scope.datastreamsList = [];

    $scope.ds_settings = {
        scrollableHeight: '200px',
        scrollable: true,
        enableSearch: true
    };

    $scope.loading = false;
    $scope.results = false;

    $http.get(getUrl() + "/v1.0/Datastreams?$select=id,name").then(function (response) {
        $scope.datastreamsList = response.data.value;
        angular.forEach($scope.datastreamsList, function(value, key){
            $scope.ds_data.push({id: value['@iot.id'], label: value['name']});
        });
    });

    $scope.supportClicked = function(sel_sup){
        $scope.newParams.minSup = sel_sup;
    }

    $scope.patternClicked = function(sel_pattern){
        $scope.newParams.patternType = sel_pattern;
    }

    $scope.open = function (content){
        var modalInstance = $uibModal.open({
          animation: true,
          ariaLabelledBy: 'modal-title',
          ariaDescribedBy: 'modal-body',
          templateUrl: content,
          controller: 'ModalInstanceCtrl',
          resolve: {
          params: function() {
            return $scope.newParams;
            }
          }
        });

        modalInstance.result.then(function(dataset){
            //$scope.loading = false;
            //$scope.results = true;
            
            //var blob = new Blob([JSON.stringify(dataset)], {type : 'application/json'});
            //saveAs(blob, "dataset.json");

            runPython(JSON.stringify(dataset)).then(function(resData){
                //stop spinner
                $scope.loading = false;
                $scope.results = true;
                alert( "added: " + JSON.stringify(resData));
                //check if resData is fine then display, otherwise show message
            });
        });
    };

    $scope.initData = function(){
        $scope.newParams.crossingList = [];
        if($scope.ds_model.length <= 1){
            alert("Error: select atleast 2 datastreams");
        }else{
            // fetch datastream observations
            getObservations($scope.ds_model).then(function(crossingList){
                $scope.newParams.crossingList = crossingList;
                //stop spinner
                $scope.loading = false;
                $scope.results = false;

                //2. Request for extraction of gradual patterns
                if($scope.newParams.patternType === "gradual"){
                    //alert("pattern type: "+$scope.newParams.patternType);
                    $scope.open('gradualContent.html');
                }else if($scope.newParams.patternType === "emerging"){
                    //alert("pattern type: "+$scope.newParams.patternType);
                    $scope.open('emergingContent.html');
                }else{
                    var msg = "Error: unable to resolve request, please reload page";
                    alert(msg);
                    $scope.info_msg = msg;
                }
            });              
        }
    }

    $scope.getDatastreamName = function(id){
        angular.forEach($scope.ds_data, function(value, key){
            if(value.id === id){
                return value.label;
            }
        });
    }

    var getObservations = function(data_model){
        // start spinner
        $scope.loading = true;
        $scope.results = false;
        var crossingList = [];
        var deferred = $q.defer();

        angular.forEach(data_model, function(value, key){
            //1. Load selected datastreams' observations
            var res = $http.get(getUrl() + "/v1.0/Datastreams("+ value.id +")/Observations?$top=1000&$orderby=phenomenonTime desc&$select=id,phenomenonTime,result");
            res.success(function(data, status, headers, config) {
                var observationList = data.value;
                var tempList = [];
                angular.forEach(observationList, function(val, k){
                    var tempObsv = {"time" : val['phenomenonTime'], "value" : val['result']};
                    tempList.push(tempObsv)
                });
                crossingList.push({id: value.id, name: $scope.getDatastreamName(value.id), observations: tempList});
            });
            res.error(function(data, status, headers, config) {
                var msg = "Data crossing failure: " + status;
                $scope.loading = false;
                $scope.results = false;
                //alert(msg);
                $scope.info_msg = msg;
                deferred.reject(msg);
            });
        });
        deferred.resolve(crossingList);
        return deferred.promise;
    }

    var runPython = function(dataset){
        //start spinner
        $scope.loading = true;
        $scope.results = false;
        var deferred = $q.defer();

        var res = $http.post(getUrl() + "/py1.0", dataset);
        res.success(function(data, status, headers, config) {
            var imgData = data;
            msg = "+ : increasing and - : decreasing and x : irrelevant";
            $scope.info_msg = msg;
            deferred.resolve(imgData);
        });
        res.error(function(data, status, headers, config) {
            //var msg = "Python API failure: "  + JSON.stringify(config);
            var msg = "Python API failure: "  + status;
            $scope.loading = false;
            $scope.results = false;
            //alert(msg);
            $scope.info_msg = msg;
            deferred.reject(msg);
        });
        return deferred.promise;
    }

});