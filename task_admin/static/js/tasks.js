app.controller('tasksController', function ($scope, $rootScope, $http, $location, $mdDialog, API, taskRunSetCreator) {

    $scope.results = [];

    $scope.selected = [];

    $scope.showTaskCreate = function (ev, task) {
        $mdDialog.show({
                controller: function DialogController($scope, $timeout, $http, $mdDialog, $mdToast) {
                    $scope.var_helps = [];
                    $http.get('/api/task_create/').then(function (response) {
                        $scope.var_helps = response.data;
                    });


                    $scope.task_name = '';
                    $scope.template_code = '';
                    $scope.is_local = true;
                    $scope.edit_mode = false;
                    if (task) {
                        $scope.task_name = task.name;
                        $scope.template_code = task.code;
                        $scope.is_local = task.is_local;
                        $scope.edit_mode = true;
                    }
                    $scope.$watch('template_code', function () {
                        var result = $scope.template_code;
                        angular.forEach($scope.var_helps, function (item) {
                            var re = new RegExp(item.template, 'g');
                            result = result.replace(re, item.rendered);
                        });
                        $scope.rendered_code = result;
                    });
                    $scope.hide = function () {
                        $mdDialog.cancel();
                    };

                    $scope.create = function () {
                        if ($scope.edit_mode) {
                            $http.put('/api/tasks/' + task.id + '/', {
                                name: $scope.task_name,
                                code: $scope.template_code,
                                is_local: $scope.is_local,
                                author: 1
                            }).then(function (response) {
                                $mdDialog.hide();
                                $mdToast.show(
                                    $mdToast.simple()
                                        .textContent('Task Saved')
                                        .position('top right')
                                        .hideDelay(6000)
                                );
                            });
                        }
                        else {
                            $http.post('/api/tasks/', {
                                name: $scope.task_name,
                                code: $scope.template_code,
                                is_local: $scope.is_local,
                                author: 1
                            }).then(function (response) {
                                $mdDialog.hide();
                                $mdToast.show(
                                    $mdToast.simple()
                                        .textContent('Task Created')
                                        .position('top right')
                                        .hideDelay(6000)
                                );
                            });
                        }
                    };

                },
                templateUrl: _static('templates/create-task.tmpl.html'),
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true
            })
            .then(function () {
                updatePage();
            }, function () {

            });
    };

    $scope.deleteSelected = function (ev) {
        var confirm = $mdDialog.confirm()
            .title('Are you sure you want to delete ' + $scope.selected.length + ' tasks?')
            .textContent('You can\'t create task run sets with these tasks anymore')
            .ariaLabel('TaskDelete confirm')
            .targetEvent(ev)
            .ok('Delete')
            .cancel('Cancel');

        $mdDialog.show(confirm).then(function () {
            angular.forEach($scope.selected, function (item) {
                $http.delete('/api/tasks/' + item.id + '/', {}).then(function () {
                    updatePage(true);
                });
            });
        }, function () {
        });
    };

    function updatePage() {
        $scope.selected = [];
        API.Task.query({}, function (tasks) {
            $scope.results = tasks;
        });
    }

    updatePage();
});