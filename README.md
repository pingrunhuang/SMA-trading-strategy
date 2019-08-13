Python Strategy Development Test.

The attached file includes Bitcoin (symbol: BTCUSD) 5 min close price data. The columns are datetime, close and volume. The datetime is the starting time of a bar.

You are a quant analyst and working on testing a trading strategy based on simple moving average (MA) cross signal. For example, we have short MA window (5) and long MA window (30). Strategy will buy 1 BTC when short moving average line crosses above long moving average line, while sell 1 BTC when short MA crosses below long MA. 

1) Please write a Python program to load data and generate buy/sell signal and trade list based on MA Cross (5,30).  

2) Based on trading list from 1) please write a program to generate a comprehensive strategy performance report (PDF format) which includes: 
     * Equity curve plot (accumulative Profit and Loss curve)
     * Sharpe ratio
     * Sortino ratio
     * Maximum drawdown
     * Trade P&L distribution plot.

3) By using BTCUSD data, will performance improve when I introduce a risk control (`stop loss` at S%, for example, I will close my open position when return is below -5%). Please include your **program** and **report**.
    1. to solve this problems, I need to search for the meaning behind each index above

4) What's the most optimized set of three parameters (p1, p2, S) while
    p1 is the short MA window from 5 to 10
    p2 is the long MA window from 25 to 35
    S is the stop loss percentage. 
    Please attach your test **program** and **result**.




5) In practice, can I use the result in (4) to start trading? Please describe your plan if yes or no. No program and report needed. 
I don't think so

6) Is there any other trading idea how we can generate P&L by using moving average cross signal?  Please describe your idea. No program and report needed. 



Note: 
•	Please make reasonable assumptions and include these assumptions in the code.
•	Please use python programming language and you are free to use library from Anaconda.
•	Please include the complete code file. 
Thank you and have fun. 



# Assumptions:
1. Assume I have 1,000,000 USD initially, and invest them all into the bitcoin market.
2. For computing the sharpe ratio, I used the risk free rate of 2018
3. 


# improvement:
1. take volume into account (https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/vama)
2. 

# Questions
1. In terms of the columns meaning, I imagine the close is the close price of bitcoin on a certain date. What about the volume, does it mean the volume of bitcoin that exists in the market or the volume that me as a trader hold? Cause I think eventually this will affect how I calculate the Equity curve.
2. For the strategy, is the MA generated according to the close price?
3. How do we deal with the Nan value of the MA?
4. For problem 1, just to clarify, whenever the short MA is higher then long MA, we need to buy one 1 bitcoin right? Suppose the short MA is always higher then the long MA during 2017-12-01 to 2017-12-31, does that mean we need to generate a buy signal everyday? (So in this case we need to buy 31 bitcoin). Same questions goes to the sell signal.
5. What do you mean trading list in problem 1? Could you give me a more concrete example? 


1. The volume means how much quantity is traded for this period. And please read carefully about the time interval of the data.
2. What else can it be? Are there any other price info available in the data set?
3. Treat them as invalid.
4. No, only when the condition changes.
5. Trade list is a list of trades. A trade is something like this: ‘I bought 1 BTC at $10,000 at 2018-08-01T00:23:21.
