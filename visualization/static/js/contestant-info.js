/**
 * Created by hamed on 4/11/17.
 */


app.directive('contestantInfo', function () {
    return {
        'scope': {
            contestant: '='
        },
        'templateUrl': _static('templates/contestant-info.tmpl.html'),
        'replace': true
    };
});