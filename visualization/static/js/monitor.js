/**
 * Created by hamed on 4/1/17.
 */

app.controller('monitorController', function ($scope, $routeParams, API) {
    $scope.rooms = [];
    API.Room.forEach(function (room) {
        if (room.name == $routeParams.name || $routeParams.name == 'all') {
            $scope.rooms.push(room);
        }
    });
});
