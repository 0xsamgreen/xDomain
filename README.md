# Cross-Domain Arbitrage Historical Viz

## Introduction
The Odos Cross-Domain Arbitrage Tracker (CAT) measures **real-time** cross-domain arbitrage opportunities between Uniswap V2 and its many clones on Ethereum and multiple L2s. The live version of the monitoring site is built and maintained by [Odos](https://www.odos.xyz) and is hosted at [https://odos.xyz/arbitrage](https://odos.xyz/arbitrage). This repo is for visualization of **historical** CAT data. It was built for ETHGlobal Paris 2023 hackathon.  

## Backend setup
1. Setup the Python environment
    ```
    cd backend
    pip install -r requirements.txt

    ```

2. Download the files in [this directory](https://drive.google.com/drive/folders/1TgLPiObFsgvXg2yxzi57aqiiujnX1h1U) and place them in `backend/assets`.

3. Start the server
    ```
    uvicorn main:app --reload
    ```

## Frontend setup
```
cd frontend
npm install --legacy-peer-deps
npm start
```

## Terminology
* *Domain* - Technically, anywhere transactions can take place (centralized exchange, decentralized exchange, order book, cash). Practically, Ethereum and various L2s.
* *Opportunity* - A cyclic arbitrage opportunity. 
* *Opportunity cluster* - Two or more opportunities that occur close together in space and value.

## Related Media
Odos CAT data was used by the following documents and presentations: 
* https://vitalik.ca/general/2021/12/06/endgame.html
* https://arxiv.org/abs/2112.01472
* https://www.youtube.com/watch?v=2iseYQwd2dA