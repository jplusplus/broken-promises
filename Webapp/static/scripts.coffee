ArticlesCtrl = ($scope, $http) =>
	$http.get('static/data/data.json').success((data) =>
		$scope.articles = data
	)

	$scope.pouet = (a) ->
		console.log('pouet', $scope.articles)

ArticleCtrl = ($scope, $http) =>



brokenPromisesApp = angular
	.module('brokenPromisesApp', [])
	.config(($routeProvider) =>
		$routeProvider
			.when('/', {controller:ListCtrl})
			.when('/article/:articleId', {controller:ArticleCtrl, templateUrl:'article.html'})
			.otherwise({redirectTo:'/'})
	)

brokenPromisesApp.controller('ArticlesCtrl', ArticlesCtrl)
