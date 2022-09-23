#!/usr/bin/env python3

# Import Libs
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup as bs
import argparse
import sys

def read_in_args():
    parser = argparse.ArgumentParser(description = 'Grab MTG card images and save them to your computer.')
    parser.add_argument('-i',metavar='deck file',action='store',help='Import an ASCII file that contains the name of MTG cards in your deck.')
    parser.add_argument('-card',action='store',help='Enter the EXACT name of the MTG card to download image.')
    args     = parser.parse_args()
    deckfile = args.i
    card     = args.card
    return deckfile,card

def write_mtg_image(name):
    url = '''https://gatherer.wizards.com/pages/search/default.aspx?name=+["{0}"]'''.format(name)
    page = requests.get(url,'html.parser')
    if page.status_code == 200:
        soup = bs(page.text,'html.parser')
        mycardsrc = soup.findAll("img", {"alt": "{0}".format(name)})
        # select src tag
        image_src = [x['src'] for x in mycardsrc]
        #print(image_src)
        # grab url
        image = 'https://gatherer.wizards.com/' + image_src[0][6:]
        # write image
        res = requests.get(image,'html.parser')
        if res.status_code == 200:
            img=Image.open(BytesIO(res.content))
            img.save('{0}.png'.format(name.replace(' ','')))
        else:
            print("Image not avaiable")
            sys.exit(1)
    else:
        print("URL not found")
        sys.exit(1)

def read_ascii_file(txtfile):
    with open(txtfile,'r') as f:
        cards = f.readlines()
    cards = [card.replace('\n','') for card in cards] # removes \n from card name
    return cards

if __name__ == '__main__':
    deckfile,card = read_in_args()
    if deckfile == None:
        print("Downloading " + card)
        write_mtg_image(card)
    else:
        decklist = read_ascii_file(deckfile)
        for card in decklist:
            print(card)
            write_mtg_image(card)

# In order to import to TTS DECCK EDITOR image sizes need to be: 672 px X 936 px
    
        
                
    
