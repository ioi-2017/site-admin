/**
 * Created by hamed on 3/19/17.
 */


var app = angular.module('NetAdmin', ['ngMaterial', 'ngResource', 'md.data.table']);

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

app.controller('NavController', function () {
    this.items = [
        { 'name': 'Monitor', 'children': ['All'] },
        { 'name': 'Admin', 'children': ['Task', 'TaskRunSets'] },
        { 'name': 'Config', 'children': ['Nodes', 'People', 'Desks']}
    ];
});