app = angular.module('Layout', ['ngMaterial', 'ngRoute', 'ngResource']);

app.directive('sideBar', function () {
    return {
        'controllerAs': 'sidebar',
        'controller': function (navigation) {
            this.contest_logo = _static('images/ioi2017.png');
            this.contest_title = 'IOI 2017';
            this.menu = navigation.getMenu();
        },
        'templateUrl': _static('templates/sidebar.tmpl.html'),
        'replace': true
    };
});

app.directive('menuLink', function () {
    return {
        'scope': {
            section: '=section',
            parent: '=parent'
        },
        'controllerAs': 'menulink',
        'controller': function () {
        },
        'templateUrl': _static('templates/menu-link.tmpl.html')
    };
});

app.directive('menuToggle', function () {
    return {
        'scope': {
            section: '=section'
        },
        'controllerAs': 'menutoggle',
        'controller': function ($scope) {
        },
        'templateUrl': _static('templates/menu-toggle.tmpl.html')
    };
});

app.directive('headBar', function () {
    return {
        'controllerAs': 'header',
        'controller': function ($rootScope, $location) {
            var headbar = this;
            this.user = 'Hamed';
            this.location = $location.path();

            $rootScope.$on('$locationChangeSuccess', function () {
                headbar.location = $location.path();
            });
        },
        'templateUrl': _static('templates/header.tmpl.html'),
        'replace': true
    };
});
