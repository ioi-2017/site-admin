app = angular.module('Layout', ['ngMaterial', 'ngResource']);

app.controller('sidebarController', function ($scope) {
    $scope.contest_logo = _static('images/ioi2017.png');
    $scope.contest_title = 'IOI 2017';
});

app.controller('headerController', function ($scope, $rootScope, $location) {
    $scope.user = 'Hamed';
    $scope.location = $location.path();

    $rootScope.$on('$locationChangeSuccess', function () {
        $scope.location = $location.path();
    });
});