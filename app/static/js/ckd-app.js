/**
 * Created by xli on 2/2/14.
 */

var ckdApp = angular.module('ckdApp', [
    'ngRoute',
    'ckdController',
    'ckdService'

]);

ckdApp.config(['$httpProvider', function ($httpProvider) {

    }]).config(['$routeProvider',
        function ($routeProvider) {
            $routeProvider.

                when('/intro', {
                    templateUrl: '../static/angular-templates/ckd_intro.html',
                    controller: 'navbar_controller'
                }).
                when('/graph', {
                    templateUrl: '../static/angular-templates/ckd_graph.html',
                    controller: 'graph_controller'
                }).
                when('/input', {
                    templateUrl: '../static/angular-templates/ckd_input.html',
                    controller: 'input_controller'
                }).
                otherwise({
                    redirectTo: '/intro'
                });
        }]);


/*
 display the High/Medium/Low label based on P value
 */
ckdApp.directive('getData', function () {

    return {
        restrict: 'C',
        replace: true,
        transclude: true,
        scope: { myData: '@myData' },
        template: '<div>' +
            '<div ng-if="myData<0.0001"><span class="label label-danger">High</span></div>' +
            '<div ng-if="myData>0.0001 && myData < 0.0005"><span class="label label-warning">Medium</span></div>' +
            '<div ng-if="myData> 0.0005"><span class="label label-info">Low</span></div>' +
            '</div>'
    }

});