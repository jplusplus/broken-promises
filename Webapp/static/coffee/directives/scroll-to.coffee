angular.module('brokenPromisesApp').directive "scrollTo", ->
	(scope, element, attrs) ->
		scope.$watch "$last", () ->
			# save scroll position
			previous_position = $(window).scrollTop()
			container = $(element.get(0).parentElement)
			setTimeout(=> # because of the final page height is not already known
				body = container.find(".body")
				$(window).scrollTo(container, attrs.scrollTo or 0, ->
					body.css {
						height: $(window).height() - 65
					}
					$('body').css {
						position : "fixed",
						top      : -container.offset().top
					}
				)
			,100)
			element.on '$destroy', =>
				$('body').css {position:"static", }
				$(window).scrollTo(previous_position)
