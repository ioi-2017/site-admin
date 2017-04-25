app.controller('taskRunsetsController', function ($scope, $http, $location, $mdDialog, API, taskRunSetCreator) {
    $scope.params = {
        state: 'all',
        owner_id: '',
        page: 1
    };
    $scope.selected = [];

    $scope.showTaskRunSetCreate = function (ev) {
        taskRunSetCreator.showTaskRunSetCreate(ev, [], function () {
            update_with_page_reset(0, 1);
        });
    };

    $scope.setPage = function (n) {
        $scope.params.page = n;
    };

    var updatePageSoft = function() {
        API.Taskrunset.query($scope.params, function (taskrunsets) {
            for (var i = 0; i < taskrunsets.length; i++) {
                if ($scope.results[i].id != taskrunsets[i].id) {
                    updatePage();
                    break;
                }
                $scope.results[i].summary = taskrunsets[i].summary;
            }
        });
    };

    API.poll(1000, $scope, function () {
        //updatePageSoft();
    });

    function updatePage(replace_state) {
        $http.get('/api/taskrunsets/',
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
    updatePage(true);
});