#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 05-Nov-2013
# Last mod : 05-Nov-2013
# -----------------------------------------------------------------------------
import collector.channels
import collector.utils
import nltk

# -----------------------------------------------------------------------------
#
#    Collect Articles
#
# -----------------------------------------------------------------------------
class CollectArticles:

	def __init__(self, channels, year, month=None, day=None):
		self.channels = [channel() for channel in collector.channels.perform_channels_import(channels)]
		self.date     = (year, month, day)

	def run(self):
		results = []
		# retrieve articles from channels
		for channel in self.channels:
			results += channel.get_articles(*self.date)
		# search dates in the body articles
		for result in results:
			result.ref_dates = self.retrieve_referenced_dates(
				text          = result.body,
				date_searched = self.date)
			pass
		return results

	@classmethod
	def retrieve_referenced_dates(cls, text, date_searched):
		references = []
		import os
		# find hints in the page
		for date_format in collector.utils.get_all_date_formats(*date_searched):
			pos = text.find(date_format)
			if pos > -1:
				tokenizer = nltk.data.load(
					"file:%s" % (
						os.path.join(os.path.dirname(__file__),
						"nltk_data/tokenizers/punkt/english.pickle")))
				for sentence in tokenizer.sentences_from_text(text):
					if date_format in sentence:
						break
					sentence = None
				reference = {
					"date"           : date_searched,
					"extract"        : sentence,
					"extracted_date" : date_format
				}
				references.append(reference)
		return references

# -----------------------------------------------------------------------------
#
# TESTS
#
# -----------------------------------------------------------------------------
import unittest

class TestOperations(unittest.TestCase):
	'''Test Class'''

	def test_get_articles(self):
		channels = (
			"collector.channels.nytimes",
			# "collector.channels.guardian",
		)
		# channels  = collector.utils.get_available_channels()

		collector = CollectArticles(channels, "2014", "1")
		results   = collector.run()
		print 
		print "results:", len(results)
		assert len(results) > 0
		for result in results:
			assert result.ref_dates
			print result.ref_dates

	def test_retrieve_referenced_dates(self):
		text = """
		It is fitting that the game that counts the most for the United States menâs soccer team â a World Cup qualifier against Mexico â also counts in the latest edition of FIFAâs world rankings, released Thursday. 
		The United States, which defeated Mexico (again), 2-0, Tuesday, and later that night earned a spot in the 2014 World Cup when Honduras and Panama tied, vaulted six spots and is now the No. 1 team in the Concacaf region, and No. 13 in the world. 
		It is the best showing for the United States in the rankings since July 2010. The American team fell as low as No. 36 in the summer of 2012, but that now seems like eons ago. 
		The United States still has two meaningless qualifiers (at least for the American team) remaining, and will probably play several international friendlies in the fall before the World Cup draw in Brazil on Dec. 6. 
		With the victory against Mexico, the United States has won 13 of its last 14 games. The stretch includes a win against Germany, victories in four of five World Cup qualifiers and an undefeated run to the Gold Cup title. 
		FIFA used the world rankings to determine the top eight seeds for the 2010 World Cup in South Africa, taking the top seven teams of the October 2009 rankings to name the group seeds, in addition to host South Africa. FIFA told MLSsoccer.com that âthe final draw procedure will only be determined following the FIFA World Cup Organizing Committee meeting which takes place on 3 December 2013 in Salvador de Bahia.
		If FIFA uses the scheme from four years ago, Argentina, Belgium, Brazil, Colombia, Germany, Italy, Spain and Uruguay will be the seeded teams. (Of those teams, only host Brazil, Argentina and Italy are assured of being in the 32-team field at present.) 
		Elsewhere in the rankings, Spain retained the top spot for the 25th consecutive month. Argentina moved up to No. 2 after clinching a spot in its 11th straight World Cup with a 5-2 win at Paraguay on Tuesday. Germany dropped a spot to third, Italy remained fourth and Colombia fell two places to No. 5. 
		The United States moved up the most among teams in the top 20, followed by Uruguay (No. 7) and Chile (No. 16), both of which gained five places. Bosnia and Herzegovina fell five places to No. 18. Mexico, which is struggling to advance to Brazil, fell one place to No. 21. 
		"""
		date = (2013, 12, None)
		refs = CollectArticles.retrieve_referenced_dates(text, date)
		assert len(refs) > 0
		for ref in refs:
			assert ref['date']           == date
			assert ref['extracted_date'] == "December 2013"

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestOperations)
	unittest.TextTestRunner(verbosity=2).run(suite)
