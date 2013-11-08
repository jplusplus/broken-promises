
MONTH_NAMES = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun",
"Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ]


angular.module('brokenPromisesApp').filter 'nl2br', () ->
	return (str) -> return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1<br />$2')

# Convert a date like [2014, 12, null] to "Dec 2014"
angular.module('brokenPromisesApp').filter 'ref_date', () ->
	(date) ->
		str = "" + date[0]
		if date[1]
			str = MONTH_NAMES[date[1]-1] + " " + str
		if date[2]
			str = date[2] + " " + str
		return str

# Convert a date like 2013-10-30T12:45:08Z to "30 Oct 2013"
angular.module('brokenPromisesApp').filter 'pub_date', () ->
	(date) ->
		date_obj = new Date(date)
		str = "#{date_obj.getDate()} #{MONTH_NAMES[date_obj.getMonth()]} #{date_obj.getFullYear()}"
		return str

angular.module("brokenPromisesApp").filter "snippet", ->
	(string ,ref_dates) ->
		if ref_dates? and ref_dates.length > 0
			for ref_date in ref_dates
				string = string.replace(ref_date['extracted_date'], "<span class=\"littlepart\">" + ref_date['extracted_date'] + "</span>")
		return string

###
Filters out all duplicate items from an array by checking the specified key
@param [key] {string} the name of the attribute of each object to compare for uniqueness
if the key is empty, the entire object will be compared
if the key === false then no filtering will be performed
@return {array}
###
angular.module("brokenPromisesApp").filter "unique", ->
	(items, filterOn) ->
		return items  if filterOn is false
		if (filterOn or angular.isUndefined(filterOn)) and angular.isArray(items)
			hashCheck = {}
			newItems = []
			extractValueToCompare = (item) ->
				if angular.isObject(item) and angular.isString(filterOn)
					item[filterOn]
				else
					item

			angular.forEach items, (item) ->
				valueToCheck = undefined
				isDuplicate = false
				i = 0

				while i < newItems.length
					if angular.equals(extractValueToCompare(newItems[i]), extractValueToCompare(item))
						isDuplicate = true
						break
					i++
				newItems.push item  unless isDuplicate

			items = newItems
		items

# EOF