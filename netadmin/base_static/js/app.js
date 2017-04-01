/**
 * Created by hamed on 3/19/17.
 */

var app = angular.module('NetAdmin', ['ngMaterial', 'ngRoute', 'ngResource', 'Layout', 'md.data.table']);

app.config(function ($mdThemingProvider, $httpProvider) {
    $mdThemingProvider.theme('default')
        .primaryPalette('grey', {
            'default': '800',
            'hue-1': '900'
        })
        .accentPalette('green')
        .backgroundPalette('grey', {
            'default': '800',
            'hue-1': '900'
        })
        .dark();

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


app.controller('RunsetsContoller', function($scope, $http, $location, $mdDialog) {
    $scope.params = {
        state: 'all',
        owner_id: '',
        page: 1
    };
    $scope.selected = [];
    $http.get('/api/tasks/', {params: {format: 'json'}}).then(function (response) {
        $scope.tasks = response.data;
    });
    $scope.setPage = function (n) {
        $scope.params.page = n;
    };
    function updatePage() {
        $http.get('/api/taskrunsets/',
                {
                    params: $scope.params
                }
        ).then(function (response) {
            $scope.pagination = response.data.pagination;
            $scope.results = response.data.results;
            $location.search($scope.params);
        });
    }

    function update_with_page_reset(newValue, oldValue) {
        if (newValue == oldValue)return;
        $scope.params.page = 1;
        $scope.selected = [];

        updatePage();
    }

    $scope.$watch("params.task", update_with_page_reset);
    $scope.$watch("params.state", update_with_page_reset);
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

    $scope.deleteSelected = function (ev) {
        var confirm = $mdDialog.confirm()
                .title('Are you sure you want to delete ' + $scope.selected.length + ' task run sets?')
                .textContent('All pending and running task runs will be stopped')
                .ariaLabel('TaskRunDelete confirm')
                .targetEvent(ev)
                .ok('Delete')
                .cancel('Cancel');

        $mdDialog.show(confirm).then(function () {
            angular.forEach($scope.selected, function (item) {
            $http.delete('/api/taskrunsets/' + item.id + '/', {}).then(function () {
                update_with_page_reset(0, 1)
            });
            });
        }, function () {
        });
    };

    $scope.owners = [
        {
            id: '1',
            name: 'admin'
        }
    ];
    $scope.params = angular.extend($scope.params, $location.search());
    updatePage();
});

app.controller('TaskRunsContoller', function($scope, $http, $location) {
    $scope.params = {
        desk: '',
        contestant: '',
        node: '',
        run_set: '',
        page: 1
    };
    $scope.selected = [];
    $scope.hovered = null;
    $http.get('/api/tasks/', {params: {format: 'json'}}).then(function (response) {
        $scope.tasks = response.data;
    });
    $scope.setPage = function (n) {
        $scope.params.page = n;
    };

    $scope.changeHovered = function (item) {
        $scope.hovered = item
    };

    function updatePage() {
        $http.get('/api/taskruns/',
                {
                    params: $scope.params
                }
        ).then(function (response) {
            $scope.pagination = response.data.pagination;
            $scope.results = response.data.results;
            $location.search($scope.params);
        });
    }

    function update_with_page_reset(newValue, oldValue) {
        if (newValue == oldValue)return;
        $scope.params.page = 1;
        $scope.selected = [];

        updatePage();
    }

    $scope.$watch("params.run_set", update_with_page_reset);
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

    $scope.owners = [
        {
            id: '1',
            name: 'admin'
        }
    ];
    $scope.params = angular.extend($scope.params, $location.search());
    updatePage();
});