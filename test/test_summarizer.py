import unittest
import summarizer


class TestSummarizer(unittest.TestCase):

    def test_get_context(self):
        self.assertEquals(summarizer.get_context(3, (1, 2, 3, 4, 5), 2),
                          (1, 2, 3, 4, 5))
        self.assertEquals(summarizer.get_context(1, (1, 2, 3, 4, 5), 2),
                          (1, 2, 3))
        self.assertEquals(summarizer.get_context(5, (1, 2, 3, 4, 5), 2),
                          (3, 4, 5))
        self.assertEquals(summarizer.get_context(3, (1, 2, 3, 4, 5), 0),
                          (3,))
        self.assertEquals(summarizer.get_context(3, (1, 2, 3, 4, 5), 1),
                          (2, 3, 4))

    def test_most_frequent_words(self):
        sentences = ['I jumped over the rainbow', 'I jumped over the box',
                     'I hopped over the fence', 'I love tipping over cows']
        frequent_words = ['jumped', 'rainbow']

        result = summarizer.most_frequent_words(sentences, frequent_words, 1)
        self.assertEquals(result, ['I jumped over the rainbow'])
        result = summarizer.most_frequent_words(sentences, frequent_words, 2)
        self.assertEquals(result, ['I jumped over the rainbow',
                                   'I jumped over the box'])

    def test_summarizer_simple(self):
        news_article1 = """ A woman and four children were wounded and their apparent attacker killed himself in a mass shooting Wednesday in Bay City, Texas.
                            The four children were flown to various hospitals, their ages and conditions were not immediately known,
                            said Lt. Andrew Lewis, spokesman with the Bay City police.
                            The female shooting victim was undergoing surgery Wednesday evening, Lewis said.
                            The shooting occurred at a residence in the city outside Houston.
                            Police responded to a call at 3:18 p.m. (4:18 p.m. ET) that a woman had been shot. When they arrived, they
                            discovered the other victims and the apparent shooter, Lewis said.
                            The suspect, a male, had died at the scene after apparently shooting himself in the head, Lewis said.
                            Detectives are working to determine the relationship of the suspected shooter and the victims, he said.  """

        # Return 1 sentence from the article
        result = summarizer.summarize(num_sentences=1, context_lines=2, text=news_article1)
        expected = {'The four children were flown to various hospitals, their ages and conditions were not immediately known, said Lt. Andrew Lewis,'\
                    ' spokesman with the Bay City police.': 
                    [' A woman and four children were wounded and their apparent attacker killed himself in a mass shooting Wednesday in Bay City, Texas.',
                     'The four children were flown to various hospitals, their ages and conditions were not immediately known, said Lt. Andrew Lewis,'\
                     ' spokesman with the Bay City police.',
                     'The female shooting victim was undergoing surgery Wednesday evening, Lewis said.', 'The shooting occurred at a residence in the city outside Houston.'
                     ]
                   }
        self.assertEqual(result, expected)


