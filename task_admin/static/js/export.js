app.controller('exportController', function ($scope, $rootScope, $http) {
    $scope.django_template = '{% for node in Nodes %}{{ node.ip }},{{ node.mac_address }}\n{% endfor %}';
    $scope.rendered_code = '';
    $scope.var_helps = {
        'Desks': 'Array of all desks',
        'Contestants': 'Array of all contestants',
        'Nodes': 'Array of all nodes',
        'node.ip': '192.168.200.10',
        'node.mac_address': '42:42:42:42:42:02',
        'node.username': 'user2',
        'contestant.name': 'Kian',
        'contestant.country': 'IR',
        'contestant.country.alpha3': 'IRN',
        'contestant.number': '1',
        'desk.contestant': 'Refers to desk contestant',
        'desk.active_node': 'Refers to desk active node',
        'desk.room': 'floor1',
        'desk.number': '3'
    };
    $scope.renderDjango = function () {
        $http.get('/api/export/', {params: {template: $scope.django_template}}).then(function (response) {
            $scope.rendered_code = response.data;
        });
    };
    var textFile = null;

    $scope.downloadTextFile = function () {
        var data = new Blob([$scope.rendered_code], {type: 'text/plain'});

        if (textFile !== null) {
            window.URL.revokeObjectURL(textFile);
        }

        var dlink = document.createElement('a');
        textFile = window.URL.createObjectURL(data);
        dlink.download = "export.txt";
        dlink.href = textFile;
        dlink.click();
        dlink.remove();
    };
});