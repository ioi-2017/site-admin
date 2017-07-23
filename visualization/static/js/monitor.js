/**
 * Created by hamed on 4/1/17.
 */

function getZone(container) {
    return Raphael(container.attr("id"), "100%", "100%");
}

function getContainer(zone) {
    return zone.canvas.parentElement;
}

function createDesk(zone, x, y, angle, width, height) {
    var parent = getContainer(zone);
    var absX = parent.offsetWidth * x, absY = parent.offsetHeight * y;
    var desk = zone.rect(absX - width / 2, absY - height / 2, width, height);
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
        var zone_element = $('#container-' + zoneData.id);
        zone_element.width(zoneData['width']);
        zone_element.parent().css('width', zoneData['width']);
        zone_element.parent().css('height', zoneData['height'] + 40);
        zone_element.css('height', zoneData['height']);

        var zone = getZone(zone_element);

        angular.forEach(zoneData['desks'], function (desk) {
            var node = desk.active_node;
            var contestant = desk.contestant;

            var deskElement = createDesk(zone, desk.x, desk.y, desk.angle, zoneData['desk_width'], zoneData['desk_height']);
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
            if (node.ip != null) {
                $scope.desks[node.ip] = deskElement;
            }
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