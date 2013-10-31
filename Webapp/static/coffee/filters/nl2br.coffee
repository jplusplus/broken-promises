angular.module('brokenPromisesApp', [])
	.filter 'nl2br', () ->
		return (str) -> return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1<br />$2')
