from bs4 import BeautifulSoup


from wordcloud import WordCloud

import nltk
nltk.download('stopwords')
import matplotlib.pyplot as plt

def clean_string(text, stemmer=None):

    """

    Exemplary function to clean strings; can be broken up into smaller functions.

    Some options, e.g. removing URLs, numbers, specific punctuation etc., can be tested
    with a respective application as leaving some pieces of information in the text
    might improve predictons in certain tasks.


    Input
    -----

    text (str)

    Output
    ------

    Cleaned text (str)

    """

    # Assert text input is string
    assert type(text) == str

    # Remove URLs
    # Defined here as words starting with or containing:
    # - www
    # - http
    url_fragments = ["www", "http"]

    for ff in url_fragments:

        input_string = " ".join(filter(lambda x: (ff in x) == False, text.split()))

    # Remove new lines (\n) and tabs (\t)
    text = input_string.replace("\n", " ")
    text = text.replace("\t", " ")

    # Remove excess white spaces
    text = " ".join(text.split())

    # Remove HTML code
    text = BeautifulSoup(text, "html.parser").text
    # See https://www.crummy.com/software/BeautifulSoup/bs4/doc/ for alternative
    # parsers and their advantages/disadvantages

    # Convert text to lower case
    text_interim = text.lower()

    # Remove numbers
    text = "".join([ii for ii in text_interim if not ii.isdigit()])

    # Replace a set of symbols with white spaces (otherwise time-varying would become
    # timevarying)
    text = text.translate(
        str.maketrans(
            """@.-:,!%/\\?()[]„“;●•·&’'”"′`′‘°–~€£$#*""",
            " " * len("""@.-:,!%/\\?()[]„“;●•·&’'”"′`′‘°–~€£$#*"""),
        )
    )

    # Remove any resulting excess white space
    text = " ".join(text.split())

    # Stemming
    if stemmer == None:
        text_output = text
    else:
        text_output = " ".join([stemmer.stem(tt) for tt in text.split()])
    
    # Return cleaned string
    return text_output

def plot_word_cloud(input_string, custom_words_to_remove, color_cloud='viridis'):
    
    """Simple helper function to plot word clouds"""
    
    word_cloud = WordCloud(background_color="white",
                           stopwords=nltk.corpus.stopwords.words('english')+custom_words_to_remove,
                           width=1000, height=600, colormap=color_cloud)
    
    word_cloud.generate(input_string)

    plt.figure(figsize=(10, 7), layout="constrained")
    plt.axis("off")
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.show()