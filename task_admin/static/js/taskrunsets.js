app.controller('taskRunsetsController', function ($scope, $rootScope, $http, $location, $mdDialog, API, taskRunSetCreator) {
    $scope.params = $location.search();
    $scope.results = [];

    var updateParams = function (newParams) {
        return angular.extend({
            state: 'all',
            owner_id: '',
            page: 1
        }, $location.search(), newParams);
    };

    var reload = function (newParams) {
        $scope.params = updateParams(newParams);
        return $location.search($scope.params);
    };

    $scope.selected = [];
    $scope.showTaskRunSetCreate = function (ev) {
        taskRunSetCreator.showTaskRunSetCreate(ev, [], function () {
            updatePage(true);
        });
    };

    $scope.setPage = function (n) {
        $scope.params.page = n;
    };

    var updatePageSoft = function() {
        API.Taskrunset.query($scope.params, function (taskrunsets) {
            if (taskrunsets.length != $scope.results.length) {
                $scope.results = taskrunsets;
                return;
            }
            for (var i = 0; i < taskrunsets.length; i++) {
                if ($scope.results[i].id != taskrunsets[i].id) {
                    $scope.results = taskrunsets;
                    break;
                }
                $scope.results[i].summary = taskrunsets[i].summary;
            }
        });
    };

    function updatePage(flush_selected) {
        if (flush_selected == true)
            $scope.selected = [];
        $scope.results = [];
        API.Taskrunset.query($scope.params, function (taskrunsets) {
            $scope.results = taskrunsets;
            API.poll(1000, $scope, function () {
                updatePageSoft();
            });
        });
    }

    var listeners = []
    listeners.push($scope.$watch("params.state", function (newValue, oldValue) {
        if (newValue == oldValue) return;
        $scope.selected = [];
        reload({'page': 1, 'state': newValue});
    }));
    listeners.push($scope.$watch("params.page", function (newValue, oldValue) {
        if (newValue == oldValue)return;
        reload({'page': newValue});
    }));
    $scope.prevPage = function () {
        $scope.params.page = parseInt($scope.params.page) - 1;
    };
    $scope.nextPage = function () {
        $scope.params.page = parseInt($scope.params.page) + 1;
    };

    $scope.stopTaskrunset = function (taskrunset) {
        $http.post('/api/taskrunsets/' + taskrunset.id + "/stop/", {});
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
                    updatePage(true);
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

    var isParamsRaw = function () {
        return !angular.equals($scope.params, updateParams());
    };

    listeners.push($rootScope.$on('$locationChangeStart', function (event) {
        if (isParamsRaw()) {
            event.preventDefault();
            reload().replace();
        }
    }));

    listeners.push($rootScope.$on('$locationChangeSuccess', function () {
        updatePage();
    }));

    if (isParamsRaw())
        reload();
    else
        updatePage();

    var unbind = $scope.$on('$destroy', function () {
        console.log('ok :{');
        angular.forEach(listeners, function (listener_unbind) {
            listener_unbind();
        });
        unbind();
    });
});