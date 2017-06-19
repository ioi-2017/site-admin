app.controller('taskRunsController', function ($scope, $rootScope, $http, $location, API, taskRunSetCreator) {
    $scope.params = $location.search();

    var updateParams = function (newParams) {
        return angular.extend({
            desk: '',
            contestant: '',
            node: '',
            status: 'ALL',
            run_set: '',
            page: 1
        }, $location.search(), newParams);
    };

    var reload = function (newParams) {
        $scope.params = updateParams(newParams);
        return $location.search($scope.params);
    };

    $scope.selected = [];
    $scope.showTaskRunSetCreate = function (ev) {
        taskRunSetCreator.showTaskRunSetCreate(ev, $scope.selected.map(function (taskrun) {
            return taskrun.node.ip
        }), function () {
            $scope.selected = [];
            updatePage(true);
        });
    };

    //$scope.selectAllRuns = function () {
    //    $http.get('/api/taskruns/',
    //        {
    //            params: angular.extend(angular.copy($scope.params), {page_size: 100000, page: 1})
    //        }
    //    ).then(function (response) {
    //        $scope.selected = [];
    //        angular.forEach(response.data.results, function (value) {
    //            $scope.selected.push(value)
    //        });
    //        updatePage(true);
    //    });
    //};

    $scope.hovered = null;
    $scope.setPage = function (n) {
        $scope.params.page = n;
    };

    $scope.changeHovered = function (item) {
        $scope.hovered = item
    };

    $scope.stopTaskrun = function (item) {
        $http.post('/api/taskruns/' + item.id + "/stop/", {});
    };

    var assignResults = function (results) {
        for (var i = 0; i < results.length; i++) {
            results[i].trimmed_code = (results[i].rendered_code.length>10 ? results[i].rendered_code.substr(0, 10) +
                            '...' : results[i].rendered_code);
            results[i].is_local_icon = results[i].is_local ? 'done' : 'clear';
        }
        $scope.results = results;
    };

    function remove_all(params)
    {
        var query_params = angular.copy(params);
        if (query_params.status == 'ALL')
            query_params.status = '';
        return query_params;
    }

    var updatePageSoft = function(callback) {
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
            callback();
        });
    };

    function updatePage(flush_selected) {
        if (flush_selected == true)
            $scope.selected = [];
        API.Taskrun.query(remove_all($scope.params), function (taskruns) {
            assignResults(taskruns);
            API.poll(1000, $scope, function (next) {
                updatePageSoft(next);
            });
        });
    }

    var listeners = [];
    listeners.push($scope.$watch("params.run_set", function (newValue, oldValue) {
        if (newValue == oldValue) return;
        $scope.selected = [];
        reload({'page': 1, 'run_set': newValue});
    }));
    listeners.push($scope.$watch("params.status", function (newValue, oldValue) {
        if (newValue == oldValue) return;
        $scope.selected = [];
        reload({'page': 1, 'status': newValue});
    }));
    listeners.push($scope.$watch("params.page", function (newValue, oldValue) {
        if (newValue == oldValue) return;
        reload({'page': newValue});
    }));
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
        angular.forEach(listeners, function (listener_unbind) {
            listener_unbind();
        });
        unbind();
    });
});