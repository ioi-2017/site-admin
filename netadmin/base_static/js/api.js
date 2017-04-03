/**
 * Created by hamed on 4/1/17.
 */

app.constant('MODELS', {
    'Room': '/api/rooms/:id/',
    'Node': '/api/nodes/:id/',
    'Desk': '/api/desks/:id/',
    'Contestant': '/api/contestants/:id/',
    'Taskrunset': '/api/taskrunsets/:id/',
    'Taskrun': '/api/taskruns/:id/',
    'Task': '/api/tasks/:id/'
});

app.service('API', function ($resource, $interval, MODELS) {
    var apiService = this;
    angular.forEach(MODELS, function (api_url, model) {
        apiService[model] = $resource(api_url, {id: '@_id'}, {update: {method: 'PUT'}}, {stripTrailingSlashes: false});

        apiService[model].forEach = function (callback, params) {
            var items = apiService[model].query(params || {}, function() {
                angular.forEach(items, function (item) {
                    callback(item);
                });
            });
        };
    });

    apiService.poll = function (duration, pollingScope, callback, destroy) {
        var pollingPromise = $interval(callback, duration);

        pollingScope.$on('$destroy', function () {
            if (pollingPromise) {
                $interval.cancel(pollingPromise);
            }
            if (destroy) {
                destroy();
            }
        });
    };
});