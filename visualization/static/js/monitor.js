/**
 * Created by hamed on 4/1/17.
 */

app.controller('monitorController', function ($scope, $stateParams, API, taskRunSetCreator) {
    $scope.rooms = [];
    API.Room.forEach(function (room) {
        if (room.name == $stateParams.name || $stateParams.name == 'all') {
            $scope.rooms.push(room);
        }
    });

    $scope.select = {
        desk: null
    };

    $scope.showTaskRunSetCreateForDesk = function(ev) {
        taskRunSetCreator.showTaskRunSetCreate(ev, [$scope.select.node.ip], function () {
        });
    };
});
