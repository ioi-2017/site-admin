app.controller('TaskRunsContoller', function ($scope, $http, $location, taskRunSetCreator) {
    $scope.params = {
        desk: '',
        contestant: '',
        node: '',
        state: 'ALL',
        run_set: '',
        page: 1
    };
    $scope.selected = [];

    $scope.showTaskRunSetCreate = function (ev) {
        taskRunSetCreator.showTaskRunSetCreate(ev, $scope.selected.map(function (taskrun) {
            return taskrun.node.ip
        }), function () {
            update_with_page_reset(0, 1);
        });
    };

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

    function updatePage(replace_state) {
        $http.get('/api/taskruns/',
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
        $scope.selected = [];

        updatePage();
    }

    $scope.$watch("params.run_set", update_with_page_reset);
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

    $scope.owners = [
        {
            id: '1',
            name: 'admin'
        }
    ];
    $scope.params = angular.extend($scope.params, $location.search());
    updatePage(true);
});