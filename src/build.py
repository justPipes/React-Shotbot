import table as table
from const import NHL_TEAMS,BASE_URL
from get import game
import logging
import init
import shotcard
import map
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
import seaborn as sns
import sqlite3

def main():
    '''
    This function will initliaze the database, shotcards, logos and player headshots
    '''
    init.main.all()
    

if __name__ == '__main__':
    main()