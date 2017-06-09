#!/usr/bin/env python
"""
Generating a word cloud for the Python Course
"""

from wordcloud import WordCloud, STOPWORDS
from scipy import misc
import re
import urllib
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from string import digits

STOPWORDS.update(('np','print', 'prints'))

# Example from https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages

#Diferents possibilitats. Provar...
address = 'http://www.scipy-lectures.org/intro/intro.html' # No surt numpy
address = 'https://www.datacamp.com/community/tutorials/python-numpy-tutorial' # No surt python
address = 'https://docs.scipy.org/doc/numpy-dev/user/quickstart.html' #No surt python però no esta malament
address = 'http://cs231n.github.io/python-numpy-tutorial/'  # Bé però el de sota m'agrada mes per ser la web de scipy
address = 'http://www.scipy.org/about.html'
address = 'http://www.scipy-lectures.org/intro/'

html = urllib.request.urlopen(address)

soup = BeautifulSoup(html)
data = soup.findAll(text=True)
     
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

digits = digits + '.' 
result = filter(visible, data)
result = [i.strip() for i in result if i.strip()]
result = (i.translate({ord(k): None for k in digits}) for i in result)
text = ''.join(result)

# Read the mask image.
mask=misc.imread('./elipsi.png')
# Generate a word cloud image
wc = WordCloud(background_color="white", mask=mask,
    stopwords=STOPWORDS)
# generate word cloud
wc.generate(text)
wc.to_file("cloud_1.png")

# Display the generated image:
# the matplotlib way:

plt.imshow(wc)
plt.axis("off")

# lower max_font_size
wc = WordCloud(max_font_size=100,background_color='white', mask=mask,
    stopwords=STOPWORDS)
wc.generate(text)
wc.to_file("cloud_2.png")
plt.figure()
plt.imshow(wc)
plt.axis("off")
plt.show()
