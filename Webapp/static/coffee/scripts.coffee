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
				# $location.path("/")
				$scope.active         = -1
				$scope.active_article = null
			else
				# $location.path("/article/" + a.$$hashKey)
				$scope.active         = 1
				$scope.active_article = a

		# $scope.vote = (article, note) ->
		# 	article.note = note
		# 	Restangular.one('articles', article._id).get().then((article) =>
		# 		article.note = note
		# 		article.put()
		# 	)

# EOF
