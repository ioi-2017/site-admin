/**
 * Created by hamed on 3/19/17.
 */


var app = angular.module('NetAdmin', ['ngMaterial', 'ngResource']);

app.config(function ($mdThemingProvider) {
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
});

app.directive('sideBar', function () {
    return {
        'controllerAs': 'sidebar',
        'controller': function () {
            this.contest_logo = _static('images/ioi2017.png');
            this.contest_title = 'IOI 2017';
        },
        'templateUrl': _static('templates/sidebar.html'),
        'replace': true
    };
});

app.controller('NavController', function () {
    this.items = [
        {'name': 'Monitor', 'children': ['All']},
        {'name': 'Admin', 'children': ['Task', 'TaskRunSets']},
        {'name': 'Config', 'children': ['Nodes', 'People', 'Desks']}
    ];
});

app.directive('headBar', function () {
    return {
        'controllerAs': 'header',
        'controller': function () {
            this.user = 'Hamed';
            this.location = 'Home';
        },
        'templateUrl': _static('templates/header.html'),
        'replace': true
    }
});