/**
 * Created by hamed on 6/2/17.
 */

app.config(function ($stateProvider) {
    $stateProvider
        .state({
            name: 'app',
            url: '/home/',
            views: {
                sidebar: {

                },
                headbar: {

                },
                content: {
                    template: '<h2>Hello World!</h2>'
                }
            }
        })
});