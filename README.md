# xDomain
Cross-Domain Arbitrage Historical Visualization. Originally built during ETHGlobal Paris, 2023.

## Introduction
The Odos Cross-Domain Arbitrage Tracker (CAT) measures **real-time** cross-domain arbitrage opportunities between Uniswap V2 and its many clones on Ethereum and multiple L2s. The live version of the monitoring site is built and maintained by [Odos](https://www.odos.xyz) and is hosted at [https://odos.xyz/arbitrage](https://odos.xyz/arbitrage). This repo is for analysis and visualization of **historical** CAT data. It was built for ETHGlobal Paris 2023 hackathon.  

## Backend setup
1. Setup the Python environment
    ```
    cd backend
    pip install -r requirements.txt

    ```

2. Download the files in [this directory](https://drive.google.com/drive/folders/1TgLPiObFsgvXg2yxzi57aqiiujnX1h1U?usp=sharing) and place them in `backend/assets`.

3. Start the server
    ```
    uvicorn main:app --reload
    ```

## Frontend setup
```
cd frontend
npm install
npm run dev
```

## Terminology
* *Domain* - Technically, transactions can occur anywhere (centralized exchange, decentralized exchange, order book, cash). Practically, Ethereum and various L2s.
* *Opportunity* - A cyclic arbitrage opportunity. 
* *Opportunity cluster* - Two or more opportunities that occur close together in space and value.

## Related Media
The following documents and presentations used Odos CAT data: 
* https://vitalik.ca/general/2021/12/06/endgame.html
* https://arxiv.org/abs/2112.01472
* https://www.youtube.com/watch?v=2iseYQwd2dA

## Warning
We have tried to make sure the data being analyzed here is accurate. However, it is highly probable that the numbers are not exact. This is caused by "hanging" RPC nodes. We will be correcting discrepancies in the future.