app.controller('templatesController', function ($scope, $rootScope, $http, $location, $mdDialog, API) {

    $scope.results = [];

    $scope.selected = [];

    $scope.showTemplateCreate = function (ev, template) {
        $mdDialog.show({
                controller: function DialogController($scope, $timeout, $http, $mdDialog, $mdToast) {
                    $scope.var_helps = [];
                    $http.get('/api/task_create/').then(function (response) {
                        $scope.var_helps = response.data;
                    });


                    $scope.template_name = '';
                    $scope.timeout = 10;
                    $scope.username = '';
                    $scope.template_code = '';
                    $scope.is_local = true;
                    $scope.edit_mode = false;
                    if (template) {
                        $scope.template_name = template.name;
                        $scope.template_code = template.code;
                        $scope.is_local = template.is_local;
                        $scope.timeout = template.timeout;
                        $scope.username = template.username;
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
                            $http.put('/api/templates/' + template.id + '/', {
                                name: $scope.template_name,
                                code: $scope.template_code,
                                is_local: $scope.is_local,
                                timeout: $scope.timeout,
                                username: $scope.username,
                                author: 1
                            }).then(function (response) {
                                $mdDialog.hide();
                                $mdToast.show(
                                    $mdToast.simple()
                                        .textContent('Template Saved')
                                        .position('top right')
                                        .hideDelay(6000)
                                );
                            });
                        }
                        else {
                            $http.post('/api/templates/', {
                                name: $scope.template_name,
                                code: $scope.template_code,
                                is_local: $scope.is_local,
                                timeout: $scope.timeout,
                                username: $scope.username,
                                author: 1
                            }).then(function (response) {
                                $mdDialog.hide();
                                $mdToast.show(
                                    $mdToast.simple()
                                        .textContent('Template Created')
                                        .position('top right')
                                        .hideDelay(6000)
                                );
                            });
                        }
                    };

                },
                templateUrl: _static('templates/create-template.tmpl.html'),
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
            .title('Are you sure you want to delete ' + $scope.selected.length + ' templates?')
            .textContent('You can\'t create task with these templates anymore')
            .ariaLabel('TemplateDelete confirm')
            .targetEvent(ev)
            .ok('Delete')
            .cancel('Cancel');

        $mdDialog.show(confirm).then(function () {
            angular.forEach($scope.selected, function (item) {
                $http.delete('/api/templates/' + item.id + '/', {}).then(function () {
                    updatePage(true);
                });
            });
        }, function () {
        });
    };

    function updatePage() {
        $scope.selected = [];
        API.Template.query({}, function (templates) {
            $scope.results = templates;
        });
    }

    updatePage();
});