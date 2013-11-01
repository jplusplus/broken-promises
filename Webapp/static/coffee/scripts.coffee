'use strict'
angular.module('brokenPromisesApp', ['restangular'])
	.config(["$sceProvider", ($sceProvider) ->
		$sceProvider.enabled(false) # unsafe mode
	])
	.config ['RestangularProvider', (RestangularProvider) ->
		RestangularProvider.setListTypeIsArray(false)
		RestangularProvider.setRestangularFields({
			id: "_id",
		})
	]

angular.module('brokenPromisesApp')
	.controller('ArticlesCtrl', ($scope, Restangular, $http, $location) =>
		$scope.active   = -1
		baseArticles    = Restangular.all('articles')

		baseArticles.getList().then((articles) =>
			$scope.articles = articles._items
		)

		$scope.setArticle = (a) ->
			if $scope.active_article == a
				# $location.path("/")
				$scope.active         = -1
				$scope.active_article = null
			else
				# $location.path("/article/" + a.$$hashKey)
				$scope.active         = 1
				$scope.active_article = a

		$scope.vote = (article, note) ->
			Restangular.one('articles', article._id).get().then((article) =>
				article.note = note
				article.put()
			)
	)
