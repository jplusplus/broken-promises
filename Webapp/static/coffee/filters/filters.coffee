
MONTH_NAMES = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun",
"Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ]


angular.module('brokenPromisesApp')
	.filter 'nl2br', () ->
		return (str) -> return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1<br />$2')

# Convert a date like [2014, 12, null] to "Dec 2014"
angular.module('brokenPromisesApp')
	.filter 'ref_date', () ->
		(date) ->
			str = "" + date[0]
			if date[1]
				str = MONTH_NAMES[date[1]-1] + " " + str
			if date[2]
				str = date[2] + " " + str
			return str

# Convert a date like 2013-10-30T12:45:08Z to "30 Oct 2013"
angular.module('brokenPromisesApp')
	.filter 'pub_date', () ->
		(date) ->
			date_obj = new Date(date)
			str = "#{date_obj.getDate()} #{MONTH_NAMES[date_obj.getMonth()]} #{date_obj.getFullYear()}"
			return str
