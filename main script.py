# -*- coding: utf-8 -*-

"""
Becca Wordcloud:
Script to take WhatsApp chats for 3 years and build visual
"""

# %%
# import packages
import numpy as np
import pandas as pd
import re
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# %%
# code taken from https://www.imrankhan.dev/pages/Exploring%20WhatsApp%20chats%20with%20Python.html

# takes WhatsApp .txt file and parses into tabular format

def parse_file(text_file):
    
    '''Convert WhatsApp chat log text file to a Pandas dataframe.'''
    
    # some regex to account for messages taking up multiple lines

    pat = re.compile(r'^(\d\d\/\d\d\/\d\d\d\d.*?)(?=^^\d\d\/\d\d\/\d\d\d\d|\Z)', re.S | re.M)

    with open(text_file, encoding='utf8') as f:

        data = [m.group(1).strip().replace('\n', ' ') for m in pat.finditer(f.read())]

 

    sender = []; message = []; datetime = []

    for row in data:

 

        # timestamp is before the first dash

        datetime.append(row.split(' - ')[0])

 

        # sender is between am/pm, dash and colon

        try:

            s = re.search('- (.*?):', row).group(1)

            sender.append(s)

        except:

            sender.append('')

 

        # message content is after the first colon

        try:

            message.append(row.split(': ', 1)[1])

        except:

            message.append('')

 

    df = pd.DataFrame(zip(datetime, sender, message), columns=['timestamp', 'sender', 'message'])

    df['timestamp'] = pd.to_datetime(df.timestamp, format='%d/%m/%Y, %H:%M')

 

    # remove events not associated with a sender

    df = df[df.sender != ''].reset_index(drop=True)

   

    return df

 

df = parse_file('Data/WhatsApp Chat with Adam.txt')

print(df)

# turn message data into one long string
text = ' '.join(df['message'].tolist())

# Create stopword list:
stopwords = set(STOPWORDS)

stopwords.update(["Media", "omitted", "https"])

# import mask
heart_mask = np.array(Image.open('Mask/heart_mask.jpg'))
 
# build wordcloud:
wordcloud = WordCloud(stopwords = stopwords, max_font_size = 100, 
    max_words = 150, background_color = "white", mask = heart_mask).generate(text)

# plot wordcloud
plt.figure()

plt.imshow(wordcloud, interpolation="bilinear")

plt.axis("off")

plt.show()

# use below code to define custom colour palette
# def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
#     return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

# use below code to change colour palette of wordcloud
# plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")