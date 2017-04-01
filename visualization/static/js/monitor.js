/**
 * Created by hamed on 4/1/17.
 */

app.directive('room', function () {
    return {
        'controllerAs': 'room',
        'controller': function ($http, $interval, $scope) {
            var room = getRoom($('#container'));

            var forEachItem = function(api, callback) {
                $http.get(api, {'format': 'json'}).then(function (response) {
                    angular.forEach(response.data, function (item) {
                        callback(item);
                    });
                });
            };

            var desks = {};
            forEachItem('/api/desks/', function (desk) {
                $http.get('/api/nodes/' + desk.active_node).then(function (response) {
                    desk.ip = response.data.ip;
                    desks[desk.ip] = createDesk(room, desk.x, desk.y, desk.angle);
                });
            });

            var refresh = function() {
                forEachItem('/api/nodes', function (node) {
                    if (node.ip in desks) {
                        desks[node.ip].attr('class', node.connected ? 'desk-ok' : 'desk-failed');
                    }
                });
            };
            var refreshPromise = $interval(refresh, 1000);

            $scope.$on('$destroy', function () {
                if (refreshPromise) {
                    $interval.cancel(refreshPromise);
                }
            });
        },
        'templateUrl': _static('templates/room.tmpl.html'),
        'replace': true
    };
});