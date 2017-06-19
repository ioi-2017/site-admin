app.controller('taskRunsetsController', function ($stateParams, $state, $scope, $timeout, $http, API, $mdToast, $mdDialog, taskRunSetCreator) {
    $scope.results = [];
    $scope.selected = [];

    $scope.filters = {
        state: ''
    };

    angular.extend($scope.filters, $stateParams);

    $scope.filter = function (field) {
        var query = {};
        query[field] = $scope.filters[field];
        $state.go('na.tasks', query);
    };

    $scope.showTaskRunSetCreate = function (ev) {
        taskRunSetCreator.showTaskRunSetCreate(ev, [], function () {
            updatePageSoft();
        });
    };

    $scope.stopTaskrunset = function (taskrunset) {
        $http.post('/api/taskrunsets/' + taskrunset.id + "/stop/", {}).then(function () {
            $mdToast.show(
                $mdToast.simple()
                    .textContent('TaskRunSet Aborted')
                    .position('top right')
                    .hideDelay(6000)
            )
        }, function () {
            $mdToast.show(
                $mdToast.simple()
                    .textContent('TaskRunSet Failed to abort!')
                    .position('top right')
                    .hideDelay(6000)
            )
        });
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
                    updatePageSoft();
                });
            });
        }, function () {
        });
    };

    var updatePageSoft = function (next) {
        API.Taskrunset.query($stateParams, function (taskrunsets) {
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
            if (next) next();
        });
    };

    $scope.results = API.Taskrunset.query($stateParams, function () {
        $timeout(function () {
            API.poll(1000, $scope, function (next) {
                updatePageSoft(next);
            });
        });
    });
});