/**
 * Created by hamed on 3/30/17.
 */

app.constant('NAV', [
    {
        name: 'Home'
    },
    {
        name: 'Monitor',
        type: 'toggle',
        items: [
            {
                name: 'All',
                urlPattern: '/monitor/:name',
                controller: 'monitorController',
                template: 'monitor.tmpl.html'
            }
        ]
    },
    {
        name: 'Admin',
        type: 'toggle',
        items: [
            /*{
                name: 'Tasks',
                template: 'home.tmpl.html'
            },*/
            {
                name: 'TaskRunsets',
                template: 'taskrunsets.tmpl.html'
            },
            {
                name: 'TaskRuns',
                template: 'taskruns.tmpl.html'
            },
            {
                name: 'Tasks',
                template: 'tasks.tmpl.html'
            },
            {
                name: 'Services',
                template: 'services.tmpl.html'
            }/*,
            {
                name: 'Services',
                template: 'home.tmpl.html'
            }*/
        ]
    }/*,
    {
        name: 'Config',
        type: 'toggle',
        items: [
            {
                name: 'Nodes',
                template: 'home.tmpl.html'
            },
            {
                name: 'People',
                template: 'home.tmpl.html'
            },
            {
                name: 'Desks',
                template: 'home.tmpl.html'
            }
        ]
    }*/
]);

app.provider('navigation', function () {
    var menu, links;

    var denormalize = function (normalText) {
        return normalText.replace(/([a-zA-Z])([A-Z])/g, '$1-$2').toLowerCase();
    };

    var normalize = function (text) {
        return text.replace(/-([a-z])/g, function (all, letter) {
            return letter.toUpperCase();
        });
    };

    var defaultURL = function (parts) {
        return '/' + parts.map(denormalize).join('/') + '/';
    };

    var defaultTemplateName = function (parts) {
        return parts.map(denormalize).join('-') + '.tmpl.html';
    };

    var defaultController = function (parts) {
        return parts.map(denormalize).map(normalize).join('') + 'Controller';
    };

    var fillLink = function (item, trace) {
        trace.push(item.name);
        item.url = item.url || defaultURL(trace);
        item.urlPattern = item.urlPattern || item.url;
        item.template = item.template || defaultTemplateName(trace.slice(-1));
        item.controller = item.controller || defaultController(trace.slice(-1));
        item.type = 'link';

        links.push(item);
        return item;
    };

    this.fillMenu = function (menuJSON) {
        menu = [];
        links = [];
        angular.forEach(menuJSON, function (section) {
            if (section.type != 'toggle')
                fillLink(section, []);
            else {
                angular.forEach(section.items, function (item) {
                    fillLink(item, [section.name]);
                });
            }
            this.push(section);
        }, menu);
        return menu;
    };

    this.getLinks = function () {
        return links;
    };

    var getSection = function (name) {
        var theSection = {};
        angular.forEach(menu, function (section) {
            if (section.name == name)
                theSection = section;
        });
        return theSection;
    };

    var pushRoomsLinks = function(API, section, sample) {
        API.Room.forEach(function (room) {
            var item = {
                name: room.name,
                urlPattern: sample.urlPattern,
                template: sample.template
            };
            section.items.push(fillLink(item, [section.name]));
        });
    };

    this.$get = function (API) {
        var monitor = getSection('Monitor');
        pushRoomsLinks(API, monitor, monitor.items[0]);

        return {
            getMenu: function() {
                return menu;
            }
        };
    };
});

app.config(function ($locationProvider, $routeProvider, navigationProvider, NAV) {
    navigationProvider.fillMenu(NAV);
    angular.forEach(navigationProvider.getLinks(), function (link) {
        $routeProvider.when(link.urlPattern, {
            templateUrl: _static('templates/' + link.template),
            controller: link.controller,
            controllerAs: 'ctrl',
            reloadOnSearch: false
        });
    });

    $locationProvider.html5Mode(true);
});
