app.service('taskRunSetCreator', function ($mdDialog) {
    this.showTaskRunSetCreate = function (ev, ips, create_callback) {
        $mdDialog.show({
                controller: function DialogController($scope, $timeout, $http, $mdDialog, $mdToast) {
                    $scope.selected_ips = [];
                    $scope.nodes_filter = '';
                    $scope.all_filters = {};
                    $scope.filter_names = [];
                    $scope.var_helps = [];
                    $http.get('/api/task_create/').then(function (response) {
                        $scope.var_helps = response.data;
                    });


                    $scope.task_templates = [];
                    $scope.all_nodes = [];
                    $scope.queryTaskSearch = function (query) {
                        return query ? $scope.task_templates.filter(createFilterFor(query)) : $scope.task_templates;
                    };

                    $scope.selectedTaskItemChange = function (task) {
                        if (task) {
                            $scope.template_code = task.code;
                            $scope.is_local = task.is_local;
                            $scope.timeout = task.timeout;
                            $scope.username = task.username;
                            if ($scope.run_set_name == '')
                                $scope.run_set_name = task.display
                        }
                    };

                    function updateTasks() {
                        $http.get('/api/tasks/').then(function (response) {
                            var tasks = response.data;
                            $scope.task_templates = tasks.map(function (task) {
                                return {
                                    value: task.name.toLowerCase(),
                                    display: task.name,
                                    code: task.code,
                                    is_local: task.is_local,
                                    timeout: task.timeout,
                                    username: task.username
                                };
                            });
                        });
                    }

                    updateTasks();

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
                    $scope.run_set_name = '';
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
                        $http.post('/api/taskrunsets/', {
                            code: $scope.template_code,
                            is_local: $scope.is_local,
                            timeout: $scope.timeout,
                            username: $scope.username,
                            owner: 1,
                            ips: $scope.selected_ips.map(function (node) {
                                return node.ip;
                            }),
                            name: $scope.run_set_name
                        }).then(function (response) {
                            console.log(response);
                            $mdDialog.hide();
                            $mdToast.show(
                                $mdToast.simple()
                                    .textContent('TaskRunSet Created')
                                    .position('top right')
                                    .hideDelay(6000)
                            );
                        });
                    };

                    $scope.createTaskTemplate = function (task_name) {
                        $scope.searchTaskText = '';
                        $http.post('/api/tasks/', {
                            name: task_name,
                            code: $scope.template_code,
                            is_local: $scope.is_local,
                            author: 1
                        }).then(function () {
                            updateTasks();
                            $timeout(function () {
                                $scope.searchTaskText = task_name;
                            }, 1000)
                        });
                    };

                },
                templateUrl: _static('templates/create-taskrunset.tmpl.html'),
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