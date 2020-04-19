import warnings
import argparse

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='')
    parser.add_argument('--sqlroot', type=str, default='root')
    parser.add_argument('--sqlpassword', type=str, default='')
    parser.add_argument('--sqldatabase', type=str, default='blockchain')
    args = parser.parse_args()
    return args
