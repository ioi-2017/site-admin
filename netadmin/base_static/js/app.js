/**
 * Created by hamed on 3/19/17.
 */


var app = angular.module('NetAdmin', ['ngMaterial', 'ngRoute', 'ngResource', 'Layout']);

app.config(['$mdThemingProvider', function ($mdThemingProvider) {
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
}]);
