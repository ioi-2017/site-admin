app.controller('taskRunsController', function ($stateParams, $state, $scope, $timeout, $http, API, $mdToast, taskCreator) {
    $scope.results = [];
    $scope.selected = [];
    $scope.hovered = null;

    $scope.filters = {
        status: 'ALL',
        task: -1,
        node: 0,
        desk: 0,
        contestant: 0
    };

    angular.extend($scope.filters, $stateParams);

    $scope.filter = function(field) {
        var query = {};
        query[field] = $scope.filters[field];
        $state.go('na.taskruns', query);
    };

    $scope.showTaskCreate = function (ev) {
        taskCreator.showTaskCreate(ev, $scope.selected.map(function (taskrun) {
            return taskrun.node.ip
        }), function () {
            updatePageSoft();
        });
    };

    $scope.changeHovered = function (item) {
        $scope.hovered = item
    };

    $scope.stopTaskrun = function (item) {
        $http.post('/api/taskruns/' + item.id + "/stop/", {}).then(function () {
            $mdToast.show(
                $mdToast.simple()
                    .textContent('Taskrun Aborted')
                    .position('top right')
                    .hideDelay(6000)
            )
        }, function () {
            $mdToast.show(
                $mdToast.simple()
                    .textContent('Taskrun Failed to abort!')
                    .position('top right')
                    .hideDelay(6000)
            )
        });
    };

    var assignResults = function (results) {
        for (var i = 0; i < results.length; i++) {
            results[i].trimmed_code = (results[i].rendered_code.length>10 ? results[i].rendered_code.substr(0, 10) +
                            '...' : results[i].rendered_code);
            results[i].is_local_icon = results[i].is_local ? 'done' : 'clear';
        }
        $scope.results = results;
    };

    function remove_all(params) {
        var query_params = angular.copy(params);
        if (query_params.status == 'ALL')
            query_params.status = '';
        return query_params;
    }

    var updatePageSoft = function(next) {
        API.Taskrun.query(remove_all($stateParams), function (taskruns) {
            if (taskruns.length != $scope.results.length) {
                assignResults(taskruns);
                return;
            }
            for (var i = 0; i < taskruns.length; i++) {
                if ($scope.results[i].id != taskruns[i].id) {
                    assignResults(taskruns);
                    break;
                }
                $scope.results[i].status = taskruns[i].status;
            }
            if (next) next();
        });
    };

    API.Taskrun.query(remove_all($stateParams), function (taskruns) {
        assignResults(taskruns);
        $timeout(function () {
            API.poll(1000, $scope, function (next) {
                updatePageSoft(next);
            });
        });
    });
});