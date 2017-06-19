app.controller('nodeGroupsController', function ($scope, $rootScope, $http, $location, $mdDialog, API) {
    $scope.results = [];
    $scope.showNodeGroupCreate = function (ev, nodegroup) {
        $mdDialog.show({
                controller: function DialogController($scope, $timeout, $http, $mdDialog, $mdToast) {
                    $scope.all_filters = {};
                    $scope.filter_names = [];
                    $scope.selected_ips = [];
                    $scope.selected_tab = 0;
                    $scope.nodegroup = {'expression': '', 'name': ''};
                    $scope.edit_mode = false;
                    if (nodegroup) {
                        $scope.nodegroup = nodegroup;
                        $scope.edit_mode = true;
                    }
                    $http.get('/api/nodegroups/').then(function (response) {
                        $scope.default_filter = response.data[0].name;
                        $scope.nodes_filter = $scope.default_filter; //Name of the first filter
                        angular.forEach(response.data, function (filter) {
                            $scope.all_filters[filter.name] = filter.nodes;
                            $scope.filter_names.push(filter.name);
                        });
                    });

                    $scope.evaluate_expression = function () {
                        $http.get('/api/nodegroups_render/', {
                            params: {expression: $scope.nodegroup.expression}
                        }).then(function (response) {
                            $scope.selected_ips = response.data;
                            $scope.selected_tab = 1;
                            $scope.nodes_filter = null;
                            setTimeout(function () {
                                $scope.nodes_filter = $scope.default_filter;
                            }, 1);
                        });

                    };

                    if ($scope.edit_mode)
                        $scope.evaluate_expression();

                    $scope.make_expression = function () {
                        $scope.nodegroup.expression = "node.ip in [" + $scope.selected_ips.map(function (f) {
                                return "'" + f.ip + "',";
                            }).join('\n') + "]";
                        $scope.selected_tab = 0;
                    };
                    $scope.hide = function () {
                        $mdDialog.cancel();
                    };

                    $scope.create = function () {
                        if ($scope.edit_mode) {
                            $http.put('/api/nodegroups/' + nodegroup.id + '/', {
                                name: $scope.nodegroup.name,
                                expression: $scope.nodegroup.expression
                            }).then(function (response) {
                                $mdDialog.hide();
                                $mdToast.show(
                                    $mdToast.simple()
                                        .textContent('NodeGroup Saved')
                                        .position('top right')
                                        .hideDelay(6000)
                                );
                            });
                        }
                        else {
                            $http.post('/api/nodegroups/', {
                                name: $scope.nodegroup.name,
                                expression: $scope.nodegroup.expression
                            }).then(function (response) {
                                $mdDialog.hide();
                                $mdToast.show(
                                    $mdToast.simple()
                                        .textContent('NodeGroup Created')
                                        .position('top right')
                                        .hideDelay(6000)
                                );
                            });
                        }
                    };

                },
                templateUrl: _static('templates/create-nodegroup.tmpl.html'),
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
            .title('Are you sure you want to delete ' + $scope.selected.length + ' node groups?')
            .textContent('This action is not reversible')
            .ariaLabel('Nodegroup delete confirm')
            .targetEvent(ev)
            .ok('Delete')
            .cancel('Cancel');

        $mdDialog.show(confirm).then(function () {
            angular.forEach($scope.selected, function (item) {
                $http.delete('/api/nodegroups/' + item.id + '/', {}).then(function () {
                    updatePage(true);
                });
            });
        }, function () {
        });
    };
    $scope.trim_code = function (code, threshold) {
        return (code.length > threshold ? code.substr(0, threshold) + '...' : code);
    };

    function updatePage() {
        $scope.selected = [];
        API.Nodegroup.query({}, function (nodegroups) {
            $scope.results = nodegroups;
        });
    }

    updatePage();
});