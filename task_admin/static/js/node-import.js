app.controller('nodeImportController', function ($scope, $rootScope, $http, $location, $mdDialog) {
    $scope.results = [];
    $scope.addNodes = function (ev) {
        var confirm = $mdDialog.confirm()
            .title('Are you sure you want to add ' + $scope.results.length + ' nodes?')
            .textContent('All these nodes will be added as connected')
            .ariaLabel('Node Add confirm')
            .targetEvent(ev)
            .ok('Upload')
            .cancel('Cancel');

        $mdDialog.show(confirm).then(function () {
            angular.forEach($scope.results, function (item) {
                $http.post('/api/nodes/', item).then(function (response) {
                    $mdDialog.hide();
                    item.imported = true;
                });
            });
        }, function () {
        });

    };
    $scope.render_results = function (results) {
        $scope.results = [];
        angular.forEach(results.data, function (item) {
            $scope.results.push({
                mac_address: item[0],
                ip: item[1],
                username: item[2],
                property_id: item[3],
                connected: false,
                imported: false
            });
        });
        $scope.$apply();
    };
    $scope.file_changed = function (input) {
        Papa.parse(input.files[0], {complete: $scope.render_results, skipEmptyLines: true});
    }
});