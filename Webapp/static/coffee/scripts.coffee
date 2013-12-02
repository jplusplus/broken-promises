'use strict'
angular.module('brokenPromisesApp', ['restangular'])
	.config(["$sceProvider", ($sceProvider) ->
		$sceProvider.enabled(false) # unsafe mode
	])
	.config(['RestangularProvider', (RestangularProvider) ->
		RestangularProvider.setListTypeIsArray(false)
		RestangularProvider.setRestangularFields({
			id: "_id",
		})
	])
# -----------------------------------------------------------------------------
#
#    NavigationCtrl
#
# -----------------------------------------------------------------------------
	.controller 'NavigationCtrl', ($scope) =>
		$scope.currentPanel = 1
		$scope.changePanel = (a) ->
			$scope.currentPanel = a

# -----------------------------------------------------------------------------
#
#    ReportsCtrl
#
# -----------------------------------------------------------------------------
	.controller 'ReportsCtrl', ($scope, Restangular) =>
		Restangular
			.all('reports')
			.getList().then (reports) =>
				$scope.reports = reports.reports

			$scope.setReport = (r) ->
				if $scope.active_report == r
					$scope.active_report = null
				else
					$scope.active_report = r

# -----------------------------------------------------------------------------
#
#    ScheduledJobsCtrl
#
# -----------------------------------------------------------------------------
	.controller 'ScheduledJobsCtrl', ($scope, Restangular) =>
		Restangular
			.all('scheduledjobs')
			.getList().then (jobs) =>
				$scope.jobs = jobs.jobs

			$scope.setJob = (job) ->
				if $scope.active_job == job
					$scope.active_job = null
				else
					$scope.active_job = job

# -----------------------------------------------------------------------------
#
#    ArticlesCtrl
#
# -----------------------------------------------------------------------------
	.controller 'ArticlesCtrl', ($scope, Restangular) =>
		$scope.active = -1
		Restangular
			.all('articles')
			.getList().then (articles) =>
				$scope.articles = articles.articles

		$scope.setArticle = (a) ->
			if $scope.active_article == a
				$scope.active         = -1
				$scope.active_article = null
			else
				$scope.active         = 1
				$scope.active_article = a

# EOF
