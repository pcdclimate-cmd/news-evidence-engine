import unittest
from related_news import terms,overlap,country_code,discover
class TestRelated(unittest.TestCase):
 def test_country(self):
  self.assertEqual(country_code('United States'),'US')
  self.assertEqual(country_code('Sweden'),'SE')
 def test_overlap(self):
  self.assertGreater(overlap('Russian minister announces major energy deal','Russian minister discusses major energy deal'),0.3)
 def test_no_search_for_generic_headline(self):
  result=discover('News update in Sweden')
  self.assertEqual(result['status'],'insufficient_terms')
if __name__=='__main__':unittest.main()
