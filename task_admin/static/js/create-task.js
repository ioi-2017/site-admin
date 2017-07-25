app.service('taskCreator', function ($mdDialog) {
    this.showTaskCreate = function (ev, ips, create_callback) {
        $mdDialog.show({
                controller: function DialogController($scope, $timeout, $http, $mdDialog, $mdToast) {
                    $scope.selected_ips = [];
                    $scope.nodes_filter = '';
                    $scope.all_filters = {};
                    $scope.filter_names = [];
                    $scope.var_helps = [];
                    $scope.error_message = '';
                    $http.get('/api/task_create/').then(function (response) {
                        $scope.var_helps = response.data;
                    });


                    $scope.task_templates = [];
                    $scope.all_nodes = [];
                    $scope.queryTemplateSearch = function (query) {
                        return query ? $scope.task_templates.filter(createFilterFor(query)) : $scope.task_templates;
                    };

                    $scope.selectedTemplateItemChange = function (template) {
                        if (template) {
                            $scope.template_code = template.code;
                            $scope.is_local = template.is_local;
                            $scope.timeout = template.timeout;
                            $scope.username = template.username;
                            if ($scope.task_name == '')
                                $scope.task_name = template.display;
                        }
                    };

                    function updateTemplates() {
                        $http.get('/api/templates/').then(function (response) {
                            var templates = response.data;
                            $scope.task_templates = templates.map(function (template) {
                                return {
                                    value: template.name.toLowerCase(),
                                    display: template.name,
                                    code: template.code,
                                    is_local: template.is_local,
                                    timeout: template.timeout,
                                    username: template.username
                                };
                            });
                        });
                    }

                    updateTemplates();

                    $http.get('/api/nodegroups/').then(function (response) {
                        $scope.nodes_filter = response.data[0].name; //Key of the first filter
                        angular.forEach(response.data, function (filter) {
                            $scope.all_filters[filter.name] = filter.nodes;
                            $scope.filter_names.push(filter.name);
                        });
                    });

                    $http.get('/api/nodes/').then(function (response) {
                        $scope.all_nodes = response.data;
                        $scope.table_nodes = angular.copy($scope.all_nodes);
                        angular.forEach($scope.all_nodes, function (item) {
                            if (ips.indexOf(item.ip) !== -1)
                                $scope.selected_ips.push(item);

                        });
                    });

                    /**
                     * Create filter function for a query string
                     */
                    function createFilterFor(query) {
                        var lowercaseQuery = angular.lowercase(query);

                        return function filterFn(task_template) {
                            return (task_template.value.indexOf(lowercaseQuery) === 0);
                        };

                    }


                    $scope.template_code = '';
                    $scope.is_local = true;
                    $scope.timeout = 10;
                    $scope.username = '';
                    $scope.task_name = '';
                    $scope.rendered_code = '';
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
                        $mdDialog.hide();
                        $http.post('/api/tasks/', {
                            code: $scope.template_code,
                            is_local: $scope.is_local,
                            timeout: $scope.timeout,
                            username: $scope.username,
                            owner: 1,
                            ips: $scope.selected_ips.map(function (node) {
                                return node.ip;
                            }),
                            name: $scope.task_name
                        }).then(function (response) {
                            $mdDialog.hide();
                            $mdToast.show(
                                $mdToast.simple()
                                    .textContent('Task Created')
                                    .position('top right')
                                    .hideDelay(6000)
                            );
                        }, function (response) {
                            $scope.error_message = response.data['detail'];
                        });
                    };

                    $scope.createTaskTemplate = function (template_name) {
                        $scope.searchTemplateText = '';
                        $http.post('/api/templates/', {
                            name: template_name,
                            code: $scope.template_code,
                            is_local: $scope.is_local,
                            timeout: $scope.timeout,
                            username: $scope.username,
                            author: 1
                        }).then(function () {
                            updateTemplates();
                            $timeout(function () {
                                $scope.searchTemplateText = template_name;
                            }, 1000)
                        });
                    };

                },
                templateUrl: _static('templates/create-task.tmpl.html'),
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true
            })
            .then(function () {
                create_callback();
            }, function () {

            });
    };
});