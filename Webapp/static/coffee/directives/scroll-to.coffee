angular.module('brokenPromisesApp').directive "scrollTo", ->
	(scope, element, attrs) ->
		scope.$watch "$last", () ->
			setTimeout(=> # because of the final page height is not already known
				$(window).scrollTo(element.get(0).parentElement, attrs.scrollTo or 0)
			,100)
