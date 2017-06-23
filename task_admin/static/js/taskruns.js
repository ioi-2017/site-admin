app.controller('taskRunsController', function ($stateParams, $state, $scope, $http, API, taskCreator) {
    $scope.results = [];
    $scope.selected = [];
    $scope.hovered = null;
    $scope.hovered_row = null;

    $scope.filters = {
        status: 'ALL',
        task: -1,
        node: 0,
        desk: 0,
        contestant: 0
    };

    angular.extend($scope.filters, $stateParams);

    $scope.filter = function (field) {
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

    $scope.changeHovered = function (event, item) {
        if ($scope.hovered_row)
            angular.element($scope.hovered_row).parent().parent().removeClass('show-info');
        $scope.hovered_row = event.target;
        angular.element($scope.hovered_row).parent().parent().addClass('show-info');
        $scope.hovered = item
    };

    $scope.stopTaskrun = function (item) {
        $http.post('/api/taskruns/' + item.id + "/stop/", {});
    };

    var assignResults = function (results) {
        var color_dict = {
            'PENDING': 'blueGrey',
            'RUNNING': 'yellow',
            'SUCCESS': 'green',
            'ABORTED': 'brown',
            'FAILED': 'red'
        };
        var icon_dict = {
            'PENDING': 'schedule',
            'RUNNING': 'sync',
            'SUCCESS': 'done',
            'ABORTED': 'pan_tool',
            'FAILED': 'clear'
        };
        for (var i = 0; i < results.length; i++) {
            results[i].is_local_icon = results[i].is_local ? 'done' : 'clear';
            results[i].status_color = color_dict[results[i].status];
            results[i].icon = icon_dict[results[i].status];
        }
        $scope.results = results;
    };

    function remove_all(params) {
        var query_params = angular.copy(params);
        if (query_params.status == 'ALL')
            query_params.status = '';
        return query_params;
    }

    var updatePageSoft = function (next) {
        API.Taskrun.query(remove_all($scope.params), function (taskruns) {
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