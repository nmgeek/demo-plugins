angular.module('ajenti.smartctl').controller 'SMARTWidgetController', ($scope) ->
    # $scope.widget is our widget descriptor here
    $scope.$on 'widget-update', ($event, id, data) ->
        if id != $scope.widget.id
            return
        $scope.value = data


angular.module('ajenti.smartctl').controller 'SMARTWidgetConfigController', ($scope) ->
    # $scope.configuredWidget is our widget descriptor here
    $scope.configuredWidget.config.device ?= '/dev/sda'
