
import unittest
import summarizer

class TestSummarizer(unittest.TestCase):
    
    def test_summarizer_simple(self):
        news_article1 = """ A woman and four children were wounded and their apparent attacker killed himself in a mass shooting Wednesday, 
                            said police in Bay City, Texas.
                            The four children were flown to various hospitals, their ages and conditions were not immediately known, 
                            said Lt. Andrew Lewis, spokesman with the Bay City police.
                            The female shooting victim was undergoing surgery Wednesday evening, Lewis said.
                            The shooting occurred at a residence in the city outside Houston.
                            Police responded to a call at 3:18 p.m. (4:18 p.m. ET) that a woman had been shot. When they arrived, they 
                            discovered the other victims and the apparent shooter, Lewis said.
                            The suspect, a male, had died at the scene after apparently shooting himself in the head, Lewis said.
                            Detectives are working to determine the relationship of the suspected shooter and the victims, he said.  """
       
        # Return 1 sentence from the article
        self.assertEquals(summarizer.summarize(sentence=1, text=news_article1),'')


