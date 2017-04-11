/**
 * Created by hamed on 4/11/17.
 */


app.directive('nodeInfo', function () {
    return {
        'scope': {
            node: '='
        },
        'templateUrl': _static('templates/node-info.tmpl.html'),
        'replace': true
    };
});