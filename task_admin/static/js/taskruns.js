app.controller('taskRunsController', function ($scope, $rootScope, $http, $location, $timeout, API, taskRunSetCreator) {
    $scope.params = $location.search();
    $scope.status_icon_map = {
        'PENDING': 'schedule',
        'PROGRESS': 'sync',
        'SUCCESS': 'done',
        'REVOKED': 'pan_tool',
        'FAILURE': 'clear'
    };
    $scope.status_color_map = {
        'PENDING': 'blueGrey-700',
        'PROGRESS': 'yellow-700',
        'SUCCESS': 'green-700',
        'REVOKED': 'blueGrey-700',
        'FAILURE': 'red-700'
    };
    $scope.status_text_map = {
        'PENDING': 'Pending',
        'PROGRESS': 'Running',
        'SUCCESS': 'Successful',
        'REVOKED': 'Stopped',
        'FAILURE': 'Internal Error'
    };

    var updateParams = function (newParams) {
        return angular.extend({
            desk: '',
            contestant: '',
            node: '',
            state: 'ALL',
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
        console.log(item);
        $scope.hovered = item
    };

    $scope.stopTaskrun = function (item) {
        $http.post('/api/taskruns/' + item.id + "/stop/", {});
    };

    var updatePageSoft = function () {
        $http.get('/api/taskruns/', $scope.params).then(function (taskruns) {
            taskruns = taskruns.data;
            if (taskruns.length != $scope.results.length) {
                $scope.results = taskruns;
                return;
            }
            for (var i = 0; i < taskruns.length; i++) {
                if ($scope.results[i].id != taskruns[i].id) {
                    $scope.results = taskruns;
                    return;
                }
                if ($scope.results[i].status != taskruns[i].status)
                    console.log('Status updated');
                $scope.results[i].status = taskruns[i].status;
            }
        });
    };

    API.poll(1000, $scope, function () {
        updatePageSoft();
    });

    $scope.selectedRowCallback = function (rows) {
        $scope.selected = rows;
    };


    function updatePage(flush_selected) {
        if (flush_selected == true)
            $scope.selected = [];
        $http.get('/api/taskruns/', $scope.params).then(function (taskruns) {
            $timeout(function () {
                $scope.results = taskruns.data;
                console.log('shit');
                console.log($scope.results);
                $scope.$apply();
            });
        });
    }

    $scope.$watch("params.run_set", function (newValue, oldValue) {
        if (newValue == oldValue) return;
        $scope.selected = [];
        reload({'page': 1, 'run_set': newValue});
    });
    $scope.$watch("params.status", function (newValue, oldValue) {
        if (newValue == oldValue) return;
        $scope.selected = [];
        reload({'page': 1, 'status': newValue});
    });
    $scope.$watch("params.page", function (newValue, oldValue) {
        if (newValue == oldValue) return;
        reload({'page': newValue});
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

    var isParamsRaw = function () {
        return !angular.equals($scope.params, updateParams());
    };

    $rootScope.$on('$locationChangeStart', function (event) {
        if (isParamsRaw()) {
            event.preventDefault();
            reload().replace();
        }
    });

    $rootScope.$on('$locationChangeSuccess', function () {
        updatePage();
    });

    if (isParamsRaw())
        reload();
    else
        updatePage();
});