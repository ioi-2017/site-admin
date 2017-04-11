app.service('taskRunSetCreator', function ($mdDialog) {
    this.showTaskRunSetCreate = function (ev, ips, create_callback) {
        $mdDialog.show({
                controller: function DialogController($scope, $timeout, $http, $mdDialog, $mdToast) {
                    $scope.ips = Array.from(new Set(ips)).sort();
                    $scope.var_helps = [];
                    $http.get('/api/task_create/').then(function (response) {
                        $scope.var_helps = response.data;
                    });


                    $scope.task_templates = [];
                    $scope.all_nodes = [];
                    $scope.queryTaskSearch = function (query) {
                        return query ? $scope.task_templates.filter(createFilterFor(query)) : $scope.task_templates;
                    };
                    $scope.queryNodeSearch = function (query) {
                        var available_nodes = [];
                        console.log($scope.ips);
                        $scope.all_nodes.forEach(function (node) {
                            if ($scope.ips.indexOf(node.value) == -1)
                                available_nodes.push(node)
                            console.log(node.value);
                        });
                        if (available_nodes.length > 0)
                            available_nodes.unshift({value: 'all', display: 'All nodes'});
                        var result = query ? available_nodes.filter(createFilterForNode(query)) : available_nodes;
                        return result;
                    };
                    $scope.selectedTaskItemChange = function (task) {
                        if (task) {
                            $scope.template_code = task.code;
                            $scope.is_local = task.is_local;
                        }
                    };
                    $scope.selectedNodeItemChange = function (node) {
                        if (node) {
                            var items = node.value;
                            if (node.value == 'all') {
                                items = $scope.all_nodes.map(function (x) {
                                    return x.value;
                                });
                            }
                            $scope.ips = Array.from(new Set($scope.ips.concat(items))).sort();
                            $scope.searchNodeText = '';
                        }
                    };
                    $scope.removeNode = function (node) {
                        var ips_set = new Set($scope.ips);
                        ips_set.delete(node);
                        $scope.ips = Array.from(ips_set).sort();
                    };

                    function updateTasks() {
                        $http.get('/api/tasks/').then(function (response) {
                            var tasks = response.data;
                            $scope.task_templates = tasks.map(function (task) {
                                return {
                                    value: task.name.toLowerCase(),
                                    display: task.name,
                                    code: task.code,
                                    is_local: task.is_local
                                };
                            });
                        });
                    }

                    updateTasks();

                    $http.get('/api/nodes/').then(function (response) {
                        var tasks = response.data;
                        $scope.all_nodes = tasks.map(function (node) {
                            return {
                                value: node.ip,
                                display: node.ip,
                            };
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

                    function createFilterForNode(query) {
                        var lowercaseQuery = angular.lowercase(query);

                        return function filterFn(task_template) {
                            return task_template.value == 'all' || (task_template.value.indexOf(lowercaseQuery) != -1);
                        };

                    }


                    $scope.template_code = '';
                    $scope.is_local = true;
                    $scope.rendered_code = '';
                    $scope.$watch('template_code', function () {
                        $http.get('/api/code_render/', {params: {code: $scope.template_code}}).then(function (response) {
                            $scope.rendered_code = response.data;
                        });
                    });
                    $scope.hide = function () {
                        $mdDialog.cancel();
                    };

                    $scope.create = function () {
                        console.log(ips);
                        $http.post('/api/taskrunsets/', {
                            code: $scope.template_code,
                            is_local: $scope.is_local,
                            owner: 1,
                            ips: $scope.ips
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
                clickOutsideToClose: true,
            })
            .then(function () {
                create_callback();
            }, function () {

            });
    };
});