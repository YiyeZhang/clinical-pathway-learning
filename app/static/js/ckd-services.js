/**
 * Created by xli on 2/2/14.
 */
var ckdService = angular.module('ckdService', ['ngResource']);

//http://stackoverflow.com/questions/12505760/angularjs-processing-http-response-in-service
ckdService.factory('Points', function ($http) {
    var Points = {
        async: function (batchid) {
            var promise = $http({method: 'GET', timeout: standard_timeout, params: {"batchid": batchid}, url: '/ads/data/points'}).then(function (response) {
                return response.data;
            }, function (response) {
                showMessageAlert("Something is wrong, please refresh", "warning")
            })
            return promise
        }
    };
    return Points
})

ckdService.factory('Task_score', function ($http) {
    var Task_score = {
        async: function () {
            var promise = $http({method: 'GET', timeout: standard_timeout, url: '/ads/data/task_scores'}).then(function (response) {
                return response.data;
            }, function (response) {
                showMessageAlert("Something is wrong, please refresh", "warning")
            })
            return promise
        }
    };
    return Task_score
})

ckdService.factory('Task_Group', function ($http) {


    var Task_group = {
        async: function () {
            var promise = $http({method: 'GET', timeout: standard_timeout, url: '/ads/data/task_groups'}).then(function (response) {
                return response.data;
            }, function (response) {
                showMessageAlert("Something is wrong, please refresh", "warning")
            })
            return promise
        }
    };
    return Task_group
})

ckdService.factory('Alerts', function ($http) {
    var Alerts = {
        async: function (batchid,score_batchid) {
            var promise = $http({method: 'GET', timeout: standard_timeout, params: {"batchid": batchid,"score_batchid": score_batchid}, url: '/ads/data/alerts'})
                .then(function (response) {
                    return response.data;
                }, function (response) {
                    showMessageAlert("Something is wrong, please refresh", "warning")
                })
            return promise
        }
    };
    return Alerts
});


ckdService.factory('oneAlert', function ($http) {
    var oneAlert = {
        async: function (a) {
            var promise = $http({method: 'GET', timeout: standard_timeout, url: '/ads/data/alert/' + a
            }).then(function (response) {
                return response.data;
            }, function (response) {
                showMessageAlert("Something is wrong, please refresh", "warning")
            })
            return promise
        }
    };
    return oneAlert
})

ckdService.factory('Informed', function ($http) {
    var informed = {
        async: function (start, end) {
            var promise = $http({
                method: 'GET',
                timeout: standard_timeout,
                url: '/informed/data',
                params: {"start": start, "end": end}
            }).then(function (response) {
                return response.data;
            }, function (response) {
                showMessageAlert("Something is wrong, please refresh", "warning")
            })
            return promise
        }
    };
    return informed
})

ckdService.factory('Query', function ($http) {
    var Query = {
        async: function (a) {

            var promise = $http({method: 'GET', timeout: standard_timeout, url: '/ads/data/proxy/http://fdong-ld.linkedin.biz:12000/pinot-senseidb/resources/statistics?q=statistics&bqlRequest=' + a
            }).then(function (response) {

                return response.data;
            }, function (response) {
                showMessageAlert("Something is wrong, please refresh", "warning")
            })
            return promise
        }
    };
    return Query
})
