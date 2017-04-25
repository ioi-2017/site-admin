app.controller('taskRunsController', function ($scope, $rootScope, $http, $location, API, taskRunSetCreator) {
    $scope.params = $location.search();

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
        $scope.hovered = item
    };

    $scope.stopTaskrun = function (item) {
        $http.post('/api/taskruns/' + item.id + "/stop/", {});
    };

    var updatePageSoft = function() {
        API.Taskrun.query($scope.params, function (taskruns) {
            if (taskruns.length != $scope.results.length) {
                $scope.results = taskruns;
                return;
            }
            for (var i = 0; i < taskruns.length; i++) {
                if ($scope.results[i].id != taskruns[i].id) {
                    $scope.results = taskruns;
                    break;
                }
                $scope.results[i].status = taskruns[i].status;
            }
        });
    };

    API.poll(1000, $scope, function () {
        updatePageSoft();
    });

    function updatePage(flush_selected) {
        if (flush_selected == true)
            $scope.selected = [];
        $scope.results = [];
        API.Taskrun.query($scope.params, function (taskruns) {
            $scope.results = taskruns;
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