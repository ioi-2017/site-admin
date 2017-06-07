/**
 * Created by hamed on 4/1/17.
 */

app.constant('MODELS', {
    'Room': {
        url: '/api/rooms/:id/'
    },
    'Node': {
        url: '/api/nodes/:id/'
    },
    'Desk': {
        url: '/api/desks/:id/'
    },
    'Contestant': {
        url: '/api/contestants/:id/'
    },
    'Taskrunset': {
        url: '/api/taskrunsets/:id/',
        paginated: true
    },
    'Taskrun': {
        url: '/api/taskruns/:id/',
        paginated: true
    },
    'Task': {
        url: '/api/tasks/:id/'
    }
});

app.service('API', function ($resource, $timeout, $http, MODELS) {
    var apiService = this;

    var getMethods = function(api) {
        var methods = {
            update: {method: 'PUT'}
        };

        if (api.paginated) {
            methods.query = {
                method: 'GET',
                isArray: true,
                transformResponse: function (data, headers) {
                    var tempData = data.replace(/^\)]\}',?\n/, '').trim();
                    var jsonData = JSON.parse(tempData);
                    headers()['pagination'] = jsonData.pagination;
                    return jsonData.results;
                }
            };
        }
        return methods;
    };

    angular.forEach(MODELS, function (api, model) {
        apiService[model] = $resource(api.url, {id: '@_id'}, getMethods(api), {stripTrailingSlashes: false});

        apiService[model].forEach = function (callback, params) {
            var items = apiService[model].query(params || {}, function() {
                angular.forEach(items, function (item) {
                    callback(item);
                });
            });
        };
    });

    var currentPoll;

    apiService.poll = function (duration, pollingScope, callback, destroy) {
        if (currentPoll != undefined && currentPoll.terminate != undefined)
            currentPoll.terminate();
        currentPoll = this;
        var cancelled = false;

        var update = function () {
            callback(function () {
                if (!cancelled)
                    pollingPromise = $timeout(update, duration);
            });
        };

        var pollingPromise = $timeout(update, duration);

        var terminate = function () {
            cancelled = true;
            if (pollingPromise) {
                $timeout.cancel(pollingPromise);
            }
            if (destroy) {
                destroy();
            }
        };

        pollingScope.$on('$destroy', terminate);
    };
});