/**
 * Created by hamed on 6/2/17.
 */

app.config(function ($stateProvider, $urlRouterProvider, $locationProvider, $qProvider) {
    $urlRouterProvider.otherwise('/');

    var templateUrl = function (templateName) {
        return _static('templates/' + templateName);
    };

    $stateProvider
        .state('na', {
            url: '/',
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
        .state('na.monitor', {
            url: 'monitor/:name/',
            views: {
                'content@': {
                    templateUrl: templateUrl('monitor.tmpl.html'),
                    controller: 'monitorController'
                }
            }
        })
        .state('na.taskruns', {
            url: 'taskruns',
            views: {
                'content@': {
                    templateUrl: templateUrl('taskruns.tmpl.html'),
                    controller: 'taskRunsController'
                }
            }
        })
        .state('na.tasks', {
            url: 'tasks?state',
            views: {
                'content@': {
                    templateUrl: templateUrl('taskrunsets.tmpl.html'),
                    controller: 'taskRunsetsController'
                }
            }
        })
        .state('na.templates', {
            url: 'templates',
            views: {
                'content@': {
                    templateUrl: templateUrl('tasks.tmpl.html'),
                    controller: 'tasksController'
                }
            }
        })
        .state('na.node-import', {
            url: 'node-import',
            views: {
                'content@': {
                    templateUrl: templateUrl('node-import.tmpl.html'),
                    controller: 'nodeImportController'
                }
            }
        })
        .state('na.nodegroups', {
            url: 'nodegroups',
            views: {
                'content@': {
                    templateUrl: templateUrl('nodegroups.tmpl.html'),
                    controller: 'nodeGroupsController'
                }
            }
        })
        .state('na.export', {
            url: 'export',
            views: {
                'content@': {
                    templateUrl: templateUrl('export.tmpl.html'),
                    controller: 'exportController'
                }
            }
        });

    $locationProvider.html5Mode(true);
    $qProvider.errorOnUnhandledRejections(false);
});