/**
 * Created by hamed on 3/19/17.
 */

var app = angular.module('NetAdmin', ['ngMaterial', 'ui.router', 'ngResource', 'ngMessages', 'Layout', 'md.data.table', 'angularMoment']);

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
