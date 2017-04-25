app.controller('servicesController', function ($scope, $http, $location) {
    $scope.params = {
        node: '',
        connected: ''
    };

    $http.get('/api/pinglogs/', {params: {format: 'json'}}).then(function (response) {
        $scope.pinglogs = response.data;
    });
    $scope.setPage = function (n) {
        $scope.params.page = n;
    };

    function updatePage(replace_state) {
        $http.get('/api/pinglogs/',
            {
                params: $scope.params
            }
        ).then(function (response) {
            $scope.pagination = response.data.pagination;
            $scope.results = response.data.results;
            if (replace_state)
                $location.search($scope.params).replace();
            else
                $location.search($scope.params);
        });
    }

    function update_with_page_reset(newValue, oldValue) {
        if (newValue == oldValue)return;
        $scope.params.page = 1;
        updatePage();
    }

    $scope.$watch("params.connected", update_with_page_reset);
    $scope.$watch("params.page", function (newValue, oldValue) {
        if (newValue == oldValue)return;
        updatePage();
    });
    $scope.prevPage = function () {
        $scope.params.page = parseInt($scope.params.page) - 1;
    };
    $scope.nextPage = function () {
        $scope.params.page = parseInt($scope.params.page) + 1;
    };

    $scope.params = angular.extend($scope.params, $location.search());
    updatePage(true);
});