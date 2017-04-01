/**
 * Created by hamed on 3/30/17.
 */

app.constant("NAV", [
    {
        name: 'Home'
    },
    {
        name: 'Monitor',
        type: 'toggle',
        items: [
            {
                name: 'All',
                template: 'monitor.tmpl.html'
            }
        ]
    },
    {
        name: 'Admin',
        type: 'toggle',
        items: [
            {
                name: 'Tasks'
            },
            {
                name: 'TaskRunSets'
            },
            {
                name: 'TaskRuns'
            },
            {
                name: 'Services'
            }
        ]
    },
    {
        name: 'Config',
        type: 'toggle',
        items: [
            {
                name: 'Nodes'
            },
            {
                name: 'People'
            },
            {
                name: 'Desks'
            }
        ]
    },
    {
        name: 'About'
    }
]);

app.provider('navigation', function () {
    var menu;

    var denormalize = function (normalText) {
        return normalText.replace( /([a-zA-Z])([A-Z])/g, '$1-$2' ).toLowerCase();
    };

    var defaultURL = function (parts) {
        return '/' + parts.map(denormalize).join('/') + '/';
    };

    var defaultTemplateName = function (parts) {
        return parts.map(denormalize).join('-') + '.tmpl.html';
    };

    var fillSection = function (section) {
        section.url = section.url || defaultURL([section.name]);
        section.template = section.template || defaultTemplateName([section.name]);
        section.type = 'link';
    };

    var fillItem = function (section, item) {
        item.url = item.url || defaultURL([section.name, item.name]);
        item.template = item.template || defaultTemplateName([item.name]);
        item.type = 'link';
    };

    this.fillMenu = function (menuJSON) {
        menu = [];
        angular.forEach(menuJSON, function (section) {
            if (section.type != 'toggle') {
                fillSection(section);
            }
            else {
                angular.forEach(section.items, function (item) {
                    fillItem(section, item);
                });
            }
            this.push(section);
        }, menu);
    };

    var getSection = function (name) {
        var theSection = {};
        angular.forEach(menu, function (section) {
            if (section.name == name)
                theSection = section;
        });
        return theSection;
    };

    this.getRoutingInfo = function () {
        var routes = [];
        angular.forEach(menu, function (section) {
            if (section.type == 'toggle') {
                angular.forEach(section.items, function (item) {
                    routes.push({
                        url: item.url,
                        template: item.template
                    });
                })
            }
            else {
                routes.push({
                    url: section.url,
                    template: section.template
                });
            }
        });
        return routes;
    };

    this.$get = function ($http) {
        $http.get('/api/rooms', {'format': 'json'}).then(function (response) {
            angular.forEach(response.data, function (room) {
                var item = { name: room.name };
                fillItem(getSection('Monitor'), item);
                getSection('Monitor').items.push(item);
            });
        });

        return {
            getMenu: function() {
                return menu;
            }
        };
    };
});

app.config(function ($locationProvider, $routeProvider, navigationProvider, NAV) {
    navigationProvider.fillMenu(NAV);
    angular.forEach(navigationProvider.getRoutingInfo(), function (route) {
        $routeProvider.when(route.url, {
            templateUrl: _static('templates/' + route.template)
        });
    });

    $locationProvider.html5Mode(true);
});
