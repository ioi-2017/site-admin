/**
 * Created by hamed on 4/1/17.
 */

function getZone(container) {
    return Raphael(container.attr("id"), "100%", "100%");
}

function getContainer(zone) {
    return zone.canvas.parentElement;
}

function createDesk(zone, x, y, angle) {
    var parent = getContainer(zone);
    var absX = parent.offsetWidth * x, absY = parent.offsetHeight * y;
    var deskWidth = 40, deskHeight = 20;
    var desk = zone.rect(absX - deskWidth / 2, absY - deskHeight / 2, deskWidth, deskHeight, 2);
    desk.rotate(angle);
    return desk;
}

app.controller('monitorController', function ($scope, $stateParams, $http, $timeout, $interval, API, taskCreator) {
    $scope.zones = [];
    $scope.desks = {};

    $scope.select = {
        desk: null
    };

    $scope.showTaskCreateForDesk = function(ev) {
        taskCreator.showTaskCreate(ev, [$scope.select.node.ip], function () {
        });
    };

    function updateSoft(next) {
        API.Node.query(function (nodes) {
            for (var i = 0; i < nodes.length; i++) {
                var node = nodes[i];
                if (node.ip in $scope.desks) {
                    var style = ['desk', node.status.toLowerCase(), node.connected ? 'ok' : 'failed'];
                    if ($scope.select.desk != null && $scope.select.node.ip == node.ip)
                        style.push('selected');
                    $scope.desks[node.ip].attr('class', style.join(' '));
                }
            }
            if (next) next();
        });
    }

    function initZone(zoneData) {
        var zone = getZone($('#container-' + zoneData.id));

        angular.forEach(zoneData['desks'], function (desk) {
            var node = desk.active_node;
            var contestant = desk.contestant;

            var deskElement = createDesk(zone, desk.x, desk.y, desk.angle);
            deskElement.attr('class', 'desk unknown');
            deskElement.node.onclick = function () {
                var style = [];
                if ($scope.select.desk != null) {
                    style = $scope.select.element.attr('class').split(' ');
                    style = style.filter(function (class_name) {
                        return class_name !== 'selected';
                    });
                    $scope.select.element.attr('class', style.join(' '));
                }
                $scope.select.desk = desk;
                $scope.select.node = node;
                $scope.select.contestant = contestant;
                $scope.select.element = deskElement;
                style = deskElement.attr('class').split(' ');
                style = style.filter(function (class_name) {
                    return class_name !== 'selected';
                });
                style.push('selected');
                deskElement.attr('class', style.join(' '));
            };
            $scope.desks[node.ip] = deskElement;
        });
    }

    var query = ($stateParams['name'] == 'all'? {} : {'name': $stateParams['name']});
    $scope.zones = API.Zone.query(query, function () {
        $timeout(function () {
            angular.forEach($scope.zones, function (zone) {
                initZone(zone);
            });

            updateSoft();
            API.poll(1000, $scope, function (next) {
                updateSoft(next);
            }, function () {
                angular.forEach($scope.zones, function (zone) {
                    $('#container-' + zone.id).remove();
                });
            });
        });
    });
});