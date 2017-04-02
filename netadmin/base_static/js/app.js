/**
 * Created by hamed on 3/19/17.
 */

var app = angular.module('NetAdmin', ['ngMaterial', 'ngRoute', 'ngResource', 'Layout', 'md.data.table']);

app.config(function ($mdThemingProvider, $httpProvider) {
    $mdThemingProvider.theme('default')
        .primaryPalette('grey', {
            'default': '800',
            'hue-1': '900'
        })
        .accentPalette('green')
        .backgroundPalette('grey', {
            'default': '800',
            'hue-1': '900'
        })
        .dark();

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.service('taskRunSetCreator', function ($mdDialog) {
    this.showTaskRunSetCreate = function (ev, ips, create_callback) {
        $mdDialog.show({
                controller: function DialogController($scope, $http, $mdDialog, $mdToast) {
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


app.controller('RunsetsContoller', function ($scope, $http, $location, $mdDialog) {
    $scope.params = {
        state: 'all',
        owner_id: '',
        page: 1
    };
    $scope.selected = [];
    $http.get('/api/tasks/', {params: {format: 'json'}}).then(function (response) {
        $scope.tasks = response.data;
    });
    $scope.setPage = function (n) {
        $scope.params.page = n;
    };
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