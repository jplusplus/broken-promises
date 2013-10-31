ArticlesCtrl = ($scope, $http, $location, $filter) =>
	$http.get('static/data/data.json').success((data) =>
		$scope.articles = data
		$scope.active   = -1
	)

	$scope.setArticle = (a,b) ->
		if $scope.active_article == a
			$location.path("/")
			$scope.active         = -1
			$scope.active_article = null
		else
			$location.path("/article/" + a.$$hashKey)
			$scope.active         = 1
			$scope.active_article = a

ArticleCtrl = ($scope, $http) =>

brokenPromisesApp = angular
	.module('brokenPromisesApp')
	.config ["$sceProvider", ($sceProvider) ->
		$sceProvider.enabled(false) # unsafe mode
	] 

brokenPromisesApp.controller('ArticlesCtrl', ArticlesCtrl)
