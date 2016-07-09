/**
 * Created by xli on 2/2/14.
 */



var ckdController = angular.module('ckdController', []);

ckdController.controller('navbar_controller', function ($scope, $location) {
    $scope.isActive = function (viewLocation) {
        return viewLocation === $location.path();
    };
})

ckdController.controller('graph_controller', function ($scope, $location) {

})


ckdController.controller('input_controller', function ($scope) {
    var p = {
        age: 70,
        gender: "Male",
        weight: 140,
        visit_count: 0,
        visits_info: []
    }
    var visit_info_template = {
        diagnosis: "",
        GFR: "",
        Hemoglobin: "",
        Phosphorus: "",
        Calcium: "",
        Albumin: "",
        Creatinine: ""
    }
    $scope.input_template_diagnosis =
        [
            {name: 'Chronic Kidney Disease Stage 1'},
            {name: 'Chronic Kidney Disease Stage 2'},
            {name: 'Chronic Kidney Disease Stage 3'},
            {name: 'Chronic Kidney Disease Stage 4'},
            {name: 'Chronic Kidney Disease Stage 5'},
            {name: 'Hypertension'},
            {name: 'Diabetes'},
            {name: 'Acute Kidney Failure'}
        ];

    $scope.input_template_GFR =
        [
            {name: 'below 15', value: "below 15"},
            {name: '15-29'},
            {name: '30-59'},
            {name: '60-89'},
            {name: '90 and above'}
            
        ];
    $scope.input_template_Hemo =
        [
            {name: 'below 13.5'},
            {name: 'above 13.5'}
        ];
    $scope.input_template_Pho =
        [
            {name: 'below 2.7'},
            {name: '2.7-4.6'},
            {name: 'above 4.6'}
        ];
    $scope.input_template_Albumin =
        [
            {name: 'below 4.0'},
            // {name: '3.6-4.0'},
            // {name: '4.0-5.0'},
            {name: 'above 4.0'}
        ];
    $scope.input_template_Cal =
        [
            {name: 'below 8.4'},
            {name: '8.4-9.5'},
            {name: 'above 9.5'}
        ];
    // $scope.input_template_CO2 =
    //     [
    //         {name: 'below 23'},
    //         {name: '23-29'},
    //         {name: 'above 29'}
    //     ];
    $scope.input_template_Crt =
        [
            {name: 'below 0.5'},
            {name: '0.5-1.2'},
            {name: '12-1.6'},
            {name: '16-2.2'},
            {name: '2.2-4.2' },
            {name: 'above 4.2'}
        ];
    // $scope.input_template_Pot =
    //     [
    //         {name: 'below 3.5'},
    //         {name: '3.5-5.0'},
    //         {name: 'above 5.0'}
    //     ];


    $scope.change = function () {
        p.visits_info = []
        for (var i = 0; i < p.visit_count; i++) {
            p.visits_info.push(jQuery.extend({}, visit_info_template))
        }
        console.log("after change", p)
    };


    $scope.getTimes = function () {
        return new Array(p.visit_count);
    };

    $scope.p = p

})


var score_cell_link_template = '<div class="ngCellText"> <a href="#/points?batchid={{row.getProperty(col.field)}}">{{row.getProperty(col.field)}}</a></div>';


ckdController.controller('task_score_controllers', function (Task_score, $scope) {
    $scope.loading = true;
    Task_score.async().then(function (d) {
        $scope.tasks_score = d.task_score;
        console.log(d)
        $scope.loading = false;
    });
    var templateWithTooltip = '<div class="ngCellText fullToolTip" data-toggle="tooltip" data-original-title="{{row.getProperty(col.field)}}" >{{row.getProperty(col.field)}}</div>';
    $scope.gridOptions = {
        data: 'tasks_score',
        columnDefs: [
            {field: 'batchid', displayName: 'batch', cellTemplate: score_cell_link_template },
            {field: 'num_of_training_days', displayName: 'training days' },
            {field: 'training_end_date', displayName: 'training end', cellFilter: "date:'M/d HH:mm:ss'" },
            {field: 'periodicity', displayName: 'periodicity' },
            {field: 'seasonality', displayName: 'seasonality' },
            {field: 'order', displayName: 'order' },
            {field: 'signal_to_noise', displayName: 'signal_to_noise' },
//            {field: 'readdata_start_timestamp', displayName: 'readdata start', cellFilter: "date:'M/d HH:mm:ss'" },
//            {field: 'readdata_end_timestamp', displayName: 'readdata end', cellFilter: "date:'M/d HH:mm:ss'" },
            {field: 'time_granualarity_mins', displayName: 'time granularity' },
            {field: 'score_start_timestamp', displayName: 'start', cellFilter: "date:'M/d HH:mm:ss'"},
            {field: 'score_end_timestamp', displayName: 'end', cellFilter: "date:'M/d HH:mm:ss'" },
            {field: 'breakdowns', displayName: 'breakdowns' },
            {field: 'metrics', displayName: 'metrics' },
            {field: 'comment', displayName: 'Comment', width: "6%" }
        ],
        sortInfo: { fields: ['batchid'], directions: ['desc']},
        enableRowSelection: false,
        multiSelect: false,
        plugins: [new ngGridFlexibleHeightPlugin()]
    };

})


ckdController.controller('points_controllers', function (Points, $scope, $routeParams) {
    $scope.loading = true;
    Points.async($routeParams.batchid).then(function (d) {
        $scope.points_list = d.all_points;
        console.log(d)
        $scope.loading = false;
    });
    var templateWithTooltip = '<div class="ngCellText fullToolTip" data-toggle="tooltip" data-original-title="{{row.getProperty(col.field)}}" >{{row.getProperty(col.field)}}</div>';
    $scope.gridOptions = {
        data: 'points_list',
        columnDefs: [
            {field: 'batchid', displayName: 'batch' },
            {field: 'fabric', displayName: 'fabric' },
            {field: 'p_value', displayName: 'p_value' },
            {field: 'status', displayName: 'status' },
            {field: 'type', displayName: 'type' },
            {field: 'campaign_type', displayName: 'campaign_type' },
            {field: 'click_type', displayName: 'click_type' },
            {field: 'timestamp', displayName: 'time', cellFilter: "date:'M/d HH:mm:ss'"}
        ],
        enableRowSelection: false,
        multiSelect: false,
        plugins: [new ngGridFlexibleHeightPlugin()]
    };
})


ckdController.controller('alerts_controllers',function (Alerts, $timeout, $scope, $routeParams) {
    $scope.loading = true;
    console.log("batchid:", $routeParams.batchid)
    Alerts.async($routeParams.batchid, $routeParams.score_batchid).then(function (d) {
        $scope.loading = false;
        $scope.allAlerts = d
        $scope.table_data = d.all_alerts
        console.log($scope.allAlerts.all_alerts)
    });

    var cellInputEditableTemplate = '<input ng-class="\'colt\' + col.index" ng-input="COL_FIELD" ng-model="COL_FIELD" ng-blur="updateEntity(row)" />';
    $scope.myTemplate = '<div ng-click="row.toggleExpand()" ng-style="rowStyle(row)" class="ngAggregate">\
                                    <span class="ngAggregateText">{{row.field}}:{{row.label CUSTOM_FILTERS}} ( {{row.totalChildren()}} alerts {{AggItemsLabel}})</span>\
                                   <div class="{{row.aggClass()}}"></div>\
                               </div>';

    var linkCellTemplate = '<div class="ngCellText"> <a href="#/graph/alert/{{row.getProperty(col.field)}}">Graph</a></div>';

    var feedbackTemplate = '<div class ="ngCellText"><span><a href=""><img src="/static/images/up.png" height="25" width="25" ></a></span><span><a href=""><img src="/static/images/down.png" height="25" width="25"></a></span></div>'
    var buttonCellTemplate = '<div class="ngCellText">' + '{{ row.getProperty(col.field) }}' + '</div>'
    var pvalueCellTemplate = '<div class="getData" my-data="{{row.getProperty(col.field)}}"></div>'


    $scope.gridOptions = {
        data: 'table_data',
        columnDefs: [

//            {field: 'batchid', displayName: 'batch', width: "6%" },
            {field: 'groupid', displayName: 'event', width: "6%"},
            {
                field: 'id',
                displayName: 'Graph',
                cellTemplate: linkCellTemplate,
                width: '6%'
            },
            {field: 'timestamp', displayName: 'time', cellFilter: "date:'M/d HH:mm:ss'", width: '20%'},
            {field: 'p_value', displayName: 'P-value', width: "120"},
            {field: 'p_value', displayName: 'Severity', width: "10%", cellTemplate: pvalueCellTemplate},
            {field: 'campaign_type', displayName: 'campaign_type'},
            {field: 'click_type', displayName: 'click type'},
            {field: 'type', displayName: 'type' },
            {field: 'status', displayName: 'status'},
//
//            {field: 'annotation', displayName: 'Annotation',
//                editableCellTemplate: cellInputEditableTemplate, enableCellEdit: true },
            {field: 'annotation', displayName: 'Action',
                cellTemplate: feedbackTemplate }
        ],
//        enableCellEditOnFocus: true,
        groups: ['groupid'],
        sortInfo: {
            fields: ['p_value' ],
            directions: ['asc']
        },
        enableRowSelection: false,
        multiSelect: false,
        groupsCollapsedByDefault: true,
        plugins: [new ngGridFlexibleHeightPlugin()],
        aggregateTemplate: $scope.myTemplate
    };
    // try to update the cell, didn't success
    // probably because of the grouping
    $scope.updateEntity = function (row) {
        console.log("row", row)
        if (!$scope.save) {
            $scope.save = { promise: null, pending: false, row: null };
            console.log("create save")
        }
        $scope.save.row = row.rowIndex;
        console.log("$scope.save.row", $scope.save.row)
        if (!$scope.save.pending) {
            $scope.save.pending = true;
            $scope.save.promise = $timeout(function () {
                // $scope.list[$scope.save.row].$update();
                console.log("Here you'd save your record to the server, we're updating row: "
                    + $scope.save.row + " to be: "
                    + $scope.table_data[$scope.save.row].annotation);
                $scope.save.pending = false;

            }, 1000);
        }
    };
//    console.log($scope.gridOptions)
}).directive('ngBlur', function () {
    return function (scope, elem, attrs) {
        elem.bind('blur', function () {
            scope.$apply(attrs.ngBlur);
        });
    };
});

ckdController.controller('alert_graph_controllers',
    function ($scope, $routeParams, oneAlert, Query, Informed) {
        console.log("ckdController:alert_graph_controllers")
        $scope.loading = true

        oneAlert.async($routeParams.alert_id).then(function (alert) {

            Query.async(alert.alert.query_string).then(function (data) {

                $scope.loading = false
                d = data.elements[0].results
                //convert YYYYMMDDHHmmss to epoch seconds
                d = $.map(d, function (k) {
                    return {"x": moment(k[0], "YYYYMMDDHHmmss").unix() * 1000, "y": parseInt(k[1])}
                })

                d.sort(function (a, b) {
                    if (a.x < b.x)
                        return -1;
                    if (a.x > b.x)
                        return 1;
                    return 0;
                })

                $scope.alert_info = alert.alert
                flag_data = {}
                flag_data.x = parseInt(alert.alert['timestamp']) * 1000
                flag_data.title = "Alert"
                flag_data.text = alert.alert.p_value

                Highcharts.setOptions({
                    global: {
                        useUTC: false
                    }
                });

                $("#container").highcharts("StockChart", {
                    rangeSelector: {
                        buttonTheme: { // styles for the buttons
                            fill: 'none',
                            stroke: 'none',
                            'stroke-width': 0,
                            r: 8,
                            style: {
                                color: '#039',
                                fontWeight: 'bold'
                            },
                            states: {
                                hover: {
                                },
                                select: {
                                    fill: '#039',
                                    style: {
                                        color: 'white'
                                    }
                                }
                            }
                        },
                        inputBoxBorderColor: 'gray',
                        inputBoxWidth: 120,
                        inputBoxHeight: 18,
                        inputStyle: {
                            color: '#039',
                            fontWeight: 'bold'
                        },
                        labelStyle: {
                            color: 'silver',
                            fontWeight: 'bold'
                        },
                        inputDateFormat: '%Y-%m-%d %H:%M',
                        inputEditDateFormat: '%Y-%m-%d %H:%M',
                        buttons: [
                            {
                                type: 'minute',
                                count: 60,
                                text: '1h'
                            },
                            {
                                type: 'minute',
                                count: 360,
                                text: '6h'
                            },
                            {
                                type: 'minute',
                                count: 720,
                                text: '12h'
                            },
                            {
                                type: 'day',
                                count: 1,
                                text: '1d'
                            },
                            {
                                type: 'day',
                                count: 3,
                                text: '3d'
                            },
                            {
                                type: 'week',
                                count: 1,
                                text: '1w'
                            },
                            {
                                type: 'week',
                                count: 2,
                                text: '2w'
                            },
                            {
                                type: 'month',
                                count: 1,
                                text: '1m'
                            },
                            {
                                type: 'all',
                                text: 'all'
                            }
                        ]
                    },
                    chart: {
                        type: 'line',
                        animation: false,
                        credit: false
                    },
                    plotOptions: {
                        series: {
                            turboThreshold: 0
                        }
                    },
                    xAxis: { type: 'datetime' },
                    series: [
                        {
                            name: 'metric',
                            id: 't2',
                            data: d,
                            tooltip: {
                                valueDecimals: 1

                            }
                        },
                        {
                            type: 'flags',
                            data: [flag_data],
                            onSeries: 't2',
                            shape: 'squarepin',
                            width: 30,
                            y: -30,
                            allowPointSelect: true
                        }


                    ]
                });
                console.log(flag_data.x)
                console.log(flag_data.x / 1000 - 3600 * 2)
                console.log(flag_data.x / 1000 + 3600 * 1)
                Informed.async(flag_data.x / 1000 - 3600 * 2, flag_data.x / 1000 + 3600 * 1).then(function (data) {
                    console.log(data)
                    event_list = []
                    for (i = 0; i < data.data.length; i++) {
//                        if(true){
                        if (data.data[i].source == "") {
                            event_list.push({
                                x: data.data[i].timestamp * 1000,
                                title: data.data[i].source,
                                text: data.data[i].content
                            })
                        }
                    }
                    event_list.sort(function (a, b) {
                        if (a.x < b.x)
                            return -1;
                        if (a.x > b.x)
                            return 1;
                        return 0;
                    })
                    console.log(event_list)
                    var chart = $('#container').highcharts();
                    chart.addSeries({
                        type: 'flags',
                        data: event_list,
                        onSeries: 't2',
                        shape: 'squarepin',
                        width: 30,
                        y: -60,
                        stackDistance: 30,
                        allowPointSelect: true

                    })

                })

                /* auto zoom in */
                var chart = $('#container').highcharts();
                chart.xAxis[0].setExtremes(
                    flag_data.x - 3600000 * 5,
                    flag_data.x + 3600000 * 5
                );
                /*  end auto zoom in*/
            })
        });
    })
;

ckdController.controller('query_controllers', ['$scope', '$routeParams', 'Query', '$timeout', '$http',
    function ($scope, $routeParams, Query, $timeout, $http) {


        $scope.query_result = Query.query(
            {q: $routeParams.query_str});

        /////////
        $timeout(function () {

            d = $scope.query_result.elements[0].results

            processed_data = $.map(d, function (k) {
                return {"x": moment(k[0], "YYYYMMDDHHmmss").unix() * 1000, "y": parseInt(k[1])}
            })

            processed_data.sort(function (a, b) {
                if (a.x < b.x)
                    return -1;
                if (a.x > b.x)
                    return 1;
                return 0;
            })

            $scope.processed_data = processed_data

            Highcharts.setOptions({
                global: {
                    useUTC: false
                }
            });

            console.log("processed_data", processed_data)
            $("#container").highcharts("StockChart", {
                rangeSelector: {
                    selected: 1
                },
                chart: {type: 'line'
                },

                xAxis: { type: 'datetime' },
                series: [
                    {
                        name: 'test',
                        data: processed_data,
                        tooltip: {
                            valueDecimals: 4
                        }
                    }
                ]

            })
        }, 2000)
        /////////
    }]);


/*
 this is for display the ng-grid in full height
 */
function ngGridFlexibleHeightPlugin(opts) {
    var self = this;
    self.grid = null;
    self.scope = null;
    self.init = function (scope, grid, services) {
        self.domUtilityService = services.DomUtilityService;
        self.grid = grid;
        self.scope = scope;
        var recalcHeightForData = function () {
            setTimeout(innerRecalcForData, 1);
        };
        var innerRecalcForData = function () {
            var gridId = self.grid.gridId;
            var footerPanelSel = '.' + gridId + ' .ngFooterPanel';
            var extraHeight = self.grid.$topPanel.height() + $(footerPanelSel).height();
            var naturalHeight = self.grid.$canvas.height() + 1;
            if (opts != null) {
                if (opts.minHeight != null && (naturalHeight + extraHeight) < opts.minHeight) {
                    naturalHeight = opts.minHeight - extraHeight - 2;
                }
            }

            var newViewportHeight = naturalHeight + 30;
            if (!self.scope.baseViewportHeight || self.scope.baseViewportHeight !== newViewportHeight) {
                self.grid.$viewport.css('height', newViewportHeight + 'px');
                self.grid.$root.css('height', (newViewportHeight + extraHeight) + 'px');
                self.scope.baseViewportHeight = newViewportHeight;
                self.domUtilityService.UpdateGridLayout(self.scope, self.grid);
            }
        };
        self.scope.catHashKeys = function () {
            var hash = '',
                idx;
            for (idx in self.scope.renderedRows) {
                hash += self.scope.renderedRows[idx].$$hashKey;
            }
            return hash;
        };
        self.scope.$watch('catHashKeys()', innerRecalcForData);
        self.scope.$watch(self.grid.config.data, recalcHeightForData);
    };
}