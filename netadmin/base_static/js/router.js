/**
 * Created by hamed on 6/2/17.
 */

app.config(function($stateProvider, $urlRouterProvider, $locationProvider, $qProvider) {
    $urlRouterProvider.otherwise('/');

    var templateUrl = function (templateName) {
        return _static('templates/' + templateName);
    };

    $stateProvider
        .state('na', {
            url:'/',
            views: {
                'header': {
                    templateUrl: templateUrl('header.tmpl.html'),
                    controller: 'headerController'
                },
                'sidebar': {
                    templateUrl: templateUrl('sidebar.tmpl.html'),
                    controller: 'sidebarController'
                },
                'content': {
                    template: '<h2>Hello World!</h2>'
                }
            }
        })
        .state('na.taskruns', {
            url:'taskruns',
            views: {
                'content@': {
                    templateUrl: templateUrl('taskruns.tmpl.html'),
                    controller: 'taskRunsController'
                }
            }
        })
        .state('na.tasks', {
            url:'tasks',
            views: {
                'content@': {
                    templateUrl: templateUrl('taskrunsets.tmpl.html'),
                    controller: 'taskRunsetsController'
                }
            }
        });

    $locationProvider.html5Mode(true);
    $qProvider.errorOnUnhandledRejections(false);
});