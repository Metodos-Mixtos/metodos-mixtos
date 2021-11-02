from wordcloud import WordCloud
import matplotlib.pyplot as plt


#%% Generate WordCloud from frequencies

def generate_word_cloud(f, filename, dpi=300):
    
    """Returns a word cloud of the table of frequencies
    ---
    f: table of frequencies for each word
    filename: file name or file path to save the image as"""

    wordcloud = WordCloud(width = 1000,
        height = 1000,
        background_color = 'white',)
    wordcloud.generate_from_frequencies(frequencies=f)
    fig = plt.figure(
        figsize = (10, 7),
        #facecolor = 'k',
        #edgecolor = 'k'
    )
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
    if filename:
        fig.savefig(filename, dpi=300)