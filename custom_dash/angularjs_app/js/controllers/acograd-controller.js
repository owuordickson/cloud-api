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
      template: '<div class="results"><img data-ng-src="data:image/png;base64,{{image.base64Img}}" width="640"/></div>',
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
.directive('downloads', function () {
    return {
      restrict: 'E',
      replace:true,
      template: '<div class="downloads"><button ng-click="image.download()">Download results</button></div>',
      link: function (scope, element, attr) {
            scope.$watch('downloads', function (val) {
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
    $scope.patterns = ["gradual", "temporal gradual"];

    $scope.newParams = {};
    $scope.newParams.minSup = 0.5;
    $scope.newParams.patternType = "gradual";
    $scope.newParams.datastreams = null;

    $scope.ds_model = [];
    $scope.ds_data = [];
    $scope.observationList = [];
    $scope.datastreamsList = [];

    $scope.ds_settings = {
        scrollableHeight: '200px',
        scrollable: true,
        enableSearch: true
    };

    $scope.image = {base64Img: "", download: download};

    $http.get(getUrl() + "/v1.0/Datastreams?$select=id,name").then(function (response) {
        $scope.datastreamsList = response.data.value;
        angular.forEach($scope.datastreamsList, function(value, key){
            $scope.ds_data.push({id: value['@iot.id'], label: value['name']});
        });
        showProgress(false);
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
            //var blob = new Blob([JSON.stringify(dataset)], {type : 'application/json'});
            //saveAs(blob, "dataset.json");

            runPython(JSON.stringify(dataset)).then(function(resData){
                //check if resData is fine then display, otherwise show message
                $scope.image = {base64Img: resData, download: download};
                //stop spinner
                //showProgress(false);
                showPatterns();
                //alert( "added: " + JSON.stringify(resData));
            });
        });
    };

    $scope.initData = function(){
        $scope.newParams.datastreams = [];
        if($scope.ds_model.length <= 1){
            alert("Error: select atleast 2 datastreams");
        }else{
            // fetch datastream observations
            getObservations($scope.ds_model).then(function(crossingList){
                $scope.newParams.datastreams = crossingList;
                //stop spinner
                showProgress(false);

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
        var name = "";
        angular.forEach($scope.ds_data, function(value, key){
            if(value.id == id){
                name = value.label;
            }
        });
        return name;
    }

    var getObservations = function(data_model){
        // start spinner
        showProgress(true);

        var crossingList = [];
        var deferred = $q.defer();

        angular.forEach(data_model, function(value, key){
            //1. Load selected datastreams' observations - will change after resetting POST size
            var res = $http.get(getUrl() + "/v1.0/Datastreams("+ value.id +")/Observations?$top=1000&$orderby=phenomenonTime desc&$select=id,phenomenonTime,result");
            res.success(function(data, status, headers, config) {
                var dsName = $scope.getDatastreamName(value.id);
                var observationList = data.value;
                var tempList = [];
                angular.forEach(observationList, function(val, k){
                    var tempObsv = {"time" : val['phenomenonTime'], "value" : val['result']};
                    tempList.push(tempObsv)
                });
                crossingList.push({id: value.id, name: dsName, observations: tempList});
            });
            res.error(function(data, status, headers, config) {
                var msg = "Data crossing failure: " + status;
                showProgress(false);
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
        showProgress(true);
        var deferred = $q.defer();

        var res = $http.post(getUrl() + "/py1.0", dataset);
        res.success(function(data, status, headers, config) {
            var imgData = data;
            msg = "+ : increasing and - : decreasing";
            $scope.info_msg = msg;
            deferred.resolve(imgData);
        });
        res.error(function(data, status, headers, config) {
            //var msg = "Python API failure: "  + JSON.stringify(config);
            var msg = "Python API failure: "  + status;
            showProgress(false)
            //alert(msg);
            $scope.info_msg = msg;
            deferred.reject(msg);
        });
        return deferred.promise;
    }

    var download = function() {
        //alert(this.base64Img);
        var blob = b64toBlob(this.base64Img, 'image/png');
        saveAs(blob, 'results.png');
    }

    var b64toBlob = function(b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
          var slice = byteCharacters.slice(offset, offset + sliceSize);

          var byteNumbers = new Array(slice.length);
          for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
          }

          var byteArray = new Uint8Array(byteNumbers);

          byteArrays.push(byteArray);
        }

        var blob = new Blob(byteArrays, {type: contentType});
        return blob;
    }

    var showProgress = function(val){
        $scope.loading = val;

        $scope.results = false;
        $scope.downloads = false;
    }

    var showPatterns = function(){
        $scope.loading = false;
        $scope.results = true;
        $scope.downloads = true;
    }

});
