/**
 * Created by hamed on 2/21/17.
 */

function getRoom(container) {
    return Raphael(container.attr("id"), "100%", "100%");
}

function getContainer(room) {
    return room.canvas.parentElement;
}

function createDesk(room, x, y, angle) {
    var parent = getContainer(room);
    var absX = parent.offsetWidth * x, absY = parent.offsetHeight * y;
    var deskWidth = 40, deskHeight = 20;
    var desk = room.rect(absX - deskWidth / 2, absY - deskHeight / 2, deskWidth, deskHeight, 2);
    desk.rotate(angle);
    desk.attr("class", "desk-failed");
    return desk;
}

app.directive('room', function () {
    return {
        'controllerAs': 'room',
        'scope': {
            room: '=data'
        },
        'controller': function ($http, $interval, $timeout, $scope, API) {
            $timeout(function () {
                var container = $('#container-' + $scope.room.id);
                var room = getRoom(container);

                var desks = {};
                API.Desk.forEach(function (desk) {
                    API.Node.get({id: desk.active_node}, function (node) {
                        desks[node.ip] = createDesk(room, desk.x, desk.y, desk.angle);
                    });
                }, {room: $scope.room.id});

                API.poll(1000, $scope, function () {
                    API.Node.forEach(function (node) {
                        if (node.ip in desks) {
                            desks[node.ip].attr('class', node.connected ? 'desk-ok' : 'desk-failed');
                        }
                    });
                }, function () {
                    container.remove();
                });
            });
        },
        'templateUrl': _static('templates/room.tmpl.html'),
        'replace': true
    };
});