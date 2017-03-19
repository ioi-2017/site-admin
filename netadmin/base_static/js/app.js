/**
 * Created by hamed on 3/19/17.
 */


var app = angular.module('NetAdmin', ['ngMaterial', 'ngResource']);

app.config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
        .primaryPalette('grey', {
            'default': '700',
            'hue-1': '900'
        })
        .accentPalette('green')
        .backgroundPalette('grey', {
            'default': '700',
            'hue-1': '900'
        })
        .dark();
});

app.controller('NavController', function () {
    this.items = [
        { 'name': 'Monitor', 'children': ['All'] },
        { 'name': 'Admin', 'children': ['Task', 'TaskRunSets'] },
        { 'name': 'Config', 'children': ['Nodes', 'People', 'Desks']}
    ];
});