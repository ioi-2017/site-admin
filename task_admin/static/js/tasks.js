app.controller('tasksController', function ($stateParams, $state, $scope, $timeout, $http, API, $mdToast, $mdDialog, taskCreator) {
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

    $scope.showTaskCreate = function (ev) {
        taskCreator.showTaskCreate(ev, [], function () {
            updatePageSoft();
        });
    };

    $scope.stopTask = function (task) {
        $http.post('/api/tasks/' + task.id + "/stop/", {}).then(function () {
            $mdToast.show(
                $mdToast.simple()
                    .textContent('Task Aborted')
                    .position('top right')
                    .hideDelay(6000)
            )
        }, function () {
            $mdToast.show(
                $mdToast.simple()
                    .textContent('Task Failed to abort!')
                    .position('top right')
                    .hideDelay(6000)
            )
        });
    };

    $scope.deleteSelected = function (ev) {
        var confirm = $mdDialog.confirm()
            .title('Are you sure you want to delete ' + $scope.selected.length + ' tasks?')
            .textContent('All pending and running task runs will be stopped')
            .ariaLabel('TaskDelete confirm')
            .targetEvent(ev)
            .ok('Delete')
            .cancel('Cancel');

        $mdDialog.show(confirm).then(function () {
            angular.forEach($scope.selected, function (item) {
                $http.delete('/api/tasks/' + item.id + '/', {}).then(function () {
                    $scope.selected = [];
                    updatePageSoft();
                });
            });
        }, function () {
        });
    };

    var updatePageSoft = function (next) {
        API.Task.query($stateParams, function (tasks) {
            if (tasks.length != $scope.results.length) {
                $scope.results = tasks;
                return;
            }
            for (var i = 0; i < tasks.length; i++) {
                if ($scope.results[i].id != tasks[i].id) {
                    $scope.results = tasks;
                    break;
                }
                $scope.results[i].summary = tasks[i].summary;
            }
            if (next) next();
        });
    };

    $scope.results = API.Task.query($stateParams, function () {
        $timeout(function () {
            API.poll(1000, $scope, function (next) {
                updatePageSoft(next);
            });
        });
    });
});