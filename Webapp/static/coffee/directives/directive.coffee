angular.module('brokenPromisesApp').directive "scrollTo", ->
	(scope, element, attrs) ->
		scope.$watch "$last", () ->
			# save scroll position
			previous_position = $(window).scrollTop()
			container = $(element.get(0).parentElement)
			setTimeout(=> # because of the final page height is not already known
				body = container.find(".body")
				$(window).scrollTo(container, attrs.scrollTo or 0, ->
					$('body').css {
						position : "fixed",
						top      : -container.offset().top
					}
					body.css {
						height: $(window).height() - body.offset().top
					}
				)
			,100)
			element.on '$destroy', =>
				$('body').css {position:"static", }
				$(window).scrollTo(previous_position)

angular.module('brokenPromisesApp').directive "panelselector", ->
	set_panel = (value) ->
		$(".Panels > .wrapper").css
			left : - (value-1) * $(window).width()

	(scope, element, attrs) ->
		scope.$watch "currentPanel", (value) ->
			set_panel(value)
		$(window).bind "resize", -> set_panel(scope.currentPanel)

angular.module('brokenPromisesApp').directive "panel", ->
	c = 0
	set_size = (element) ->
		$(".Panels").css("width", $(window).width())
		$(".Panels").css("height", $(window).height() - $(".Panels").offset().top)
		$(".Panels > .wrapper").css
			width  : c * $(window).width()
		element.css("width",$(window).width())
		element.css("height",$(window).height() - $(".Panels").offset().top)

	(scope, element, attrs) ->
		c++
		set_size(element)
		$(window).bind "resize", -> set_size(element)

# EOF
