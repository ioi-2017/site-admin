/**
 * Created by hamed on 4/1/17.
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
    return desk;
}

app.controller('monitorController', function ($scope, $stateParams, $http, $timeout, $interval, API, taskRunSetCreator) {
    $scope.rooms = [];
    $scope.desks = {};

    $scope.select = {
        desk: null
    };

    $scope.showTaskRunSetCreateForDesk = function(ev) {
        taskRunSetCreator.showTaskRunSetCreate(ev, [$scope.select.node.ip], function () {
        });
    };

    function updateSoft(next) {
        API.Node.forEach(function (node) {
            if (node.ip in $scope.desks) {
                var style = ['desk', node.status.toLowerCase(), node.connected ? 'ok' : 'failed'];
                $scope.desks[node.ip].attr('class', style.join(' '));
            }
        }, {}, function () {
            if (next) next();
        });
    }

    function initRoom(roomData) {
        var room = getRoom($('#container-' + roomData.id));

        angular.forEach(roomData['desks'], function (desk) {
            var node = desk.active_node;
            var contestant = desk.contestant;

            var deskElement = createDesk(room, desk.x, desk.y, desk.angle);
            deskElement.attr("class", "desk unknown");
            deskElement.node.onclick = function () {
                $scope.select.desk = desk;
                $scope.select.node = node;
                $scope.select.contestant = contestant;
            };
            $scope.desks[node.ip] = deskElement;
        });
    }

    $scope.rooms = API.Room.query({}, function () {
        $timeout(function () {
            angular.forEach($scope.rooms, function (room) {
                initRoom(room);
            });

            updateSoft();
            API.poll(1000, $scope, function (next) {
                updateSoft(next);
            }, function () {
                angular.forEach($scope.rooms, function (room) {
                    $('#container-' + room.id).remove();
                });
            });
        });
    });
});