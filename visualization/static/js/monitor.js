/**
 * Created by hamed on 4/1/17.
 */

app.directive('room', function () {
    return {
        'controllerAs': 'room',
        'controller': function ($http, $interval, $scope, API) {
            var room = getRoom($('#container'));

            var desks = {};
            API.Desk.forEach(function (desk) {
                API.Node.for({id: desk.active_node}, function (node) {
                    desks[node.ip] = createDesk(room, desk.x, desk.y, desk.angle);
                });
            });

            API.poll(function () {
                API.Node.forEach(function (node) {
                    if (node.ip in desks) {
                        desks[node.ip].attr('class', node.connected ? 'desk-ok' : 'desk-failed');
                    }
                });
            }, 1000, $scope);
        },
        'templateUrl': _static('templates/room.tmpl.html'),
        'replace': true
    };
});