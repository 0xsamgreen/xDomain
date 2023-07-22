# Odos CAT data analysis

## Introduction
The Odos Cross-Domain Arbitrage Tracker measures (but does not capture) real-time cross-domain arbitrage opportunities between Uniswap V2 and its many clones on Ethereum and multiple L2s. The live version of the monitoring site is built and maintained by [Odos](https://www.odos.xyz) and is hosted at [https://odos.xyz/arbitrage](https://odos.xyz/arbitrage). This repo is for exploratory data analysis on recorded CAT data.

The latest summary output can be found in the most recent `.pdf` here: [project files](https://drive.google.com/drive/folders/1IlaeQgOPKzE1fyhz2FuHsdj82gOvjKZE?usp=sharing). 

## Instructions
The most important file in this repo is `explore.ipynb`. This file will show you how to interact with recorded CAT data. The most recent data can be found here:
[project files](https://drive.google.com/drive/folders/1IlaeQgOPKzE1fyhz2FuHsdj82gOvjKZE?usp=sharing). Download a `cleaned` and `metadata` file from that url (make sure to use matching dates) and change the `.csv` file names in the second cell of `explore.ipynb`.

## Terminology
* *Domain* - Technically, anywhere transactions can take place (centralized exchange, decentralized exchange, order book, cash). Practically, Ethereum and various L2s.
* *Opportunity* - A cyclic arbitrage opportunity. 
* *Opportunity cluster* - Two or more opportunities that occur close together in space and value.

## CAT has been referred to in the following 
* https://vitalik.ca/general/2021/12/06/endgame.html
* https://arxiv.org/abs/2112.01472
# ethglobal-paris-2023-xdomain
