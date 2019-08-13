# How to run program
Initialize an instance of SMAStrategy. Initialization parameters are `short=5, long=30, stop_loss=None, initial_capital=100000, file_path="./hist.BTCUSD.5m.csv"` with default value after the equation. By default, stop_loss is not applied. In order to use it, fill in the stop_loss with some negative value.

To run a single set of parameters, type in `python my_strategy.py` in terminal.

To traverse different combination of parameters, type in `python strategy_test.py` in terminal.  





# Assumption
1. Assume I have 100,000 USD initially, and invest them all into the bitcoin market. Actually not necessary assumption, just to make to figure pretty.
2. For computing the sharpe ratio, I don't know where to find the best free risk rate, therefore I assume it is 0 for such a short period















# Problem 2
Based on the parameter set `short_window=5, long_window=30, stop_loss=None` these are the performance that I generated:
1. equity curve aka cumulative Profit and Loss curve
![equity curve aka cumulative Profit and Loss curve](5_30_None/cumpnl_curve.png)
2. Sharpe ratio: `-0.0029217930893280395`
3. Sortino ratio: `-0.0035945058615631884`
4. maximum drawdown: `-0.639334614609012`
5. Trade P&L distribution plot
![Trade P&L distribution plot](5_30_None/tradepnl_distribution.png)

From the trade P&L distribution, we can tell that the most profitable period happens around 2018-01-06 to 2018-01-13 and 2018-02-10 to 2018-02-17 respectively. But after this round of investment, nearly no profit was generated. Thus it might not be a good investment to bet on. Moreover, the sharp ratio and the sortino ratio tells us that it is quite not profitable overall. Moreover, the maximum drawdown is about `64%` which also indicate that the risk is too high for investing. So without any further stop loss ristriction, it is not recommended to invest on this trading strategy based on this parameter set. However, this is just our first try of how this strategy work. Let's add on the stop loss parameter for testing. 









# Problem 3
Now let's see how this strategy perform by adding a stop loss ristriction. In this case, I pick up the one that has the highest cumulative P&L value. `short=5, long=27, stop_loss=-0.001`:

1. equity curve aka cumulative Profit and Loss curve
![equity curve aka cumulative Profit and Loss curve](figures/cumpnl_curve_5_27_-0.01.png)
2. Sharpe ratio: `0.005869319462407819`
3. Sortino ratio: `0.006988886777101038`
4. maximum drawdown: `-0.640795548227535`
5. Trade P&L distribution plot
![Trade P&L distribution plot](figures/tradepnl_distribution_5_27_-0.01.png)

Although the result of the maximum drawdown is also quite high which means it is quite risky, but I think from the perspertive of final revenue, it is still quite impresive that adding a `stop loss` restriction can enhance the overall performance to such a level especially for the `sharp ratio` and `sortino ratio`(although they are still not high enough comparing to the risk free investment). 







# Problem 4
For trying out different parameters, I store the plot in the `figures.zip` file and the corresponding parameters in the `parameters.csv` file. The corresponded code stores in the `strategy_test.py` file.
From the perspective of cumulative P&L, we can tell that the `p1=5` and `p2=27` is more likely to have better performance (go up to around **15%** of return rate on average) in the case of `stop_loss=None`, `stop_loss=-0.01` and `stop_loss=-0.015`. Therefore we can  have higher confidence of saying that choosing `p1=5` and `p2=27` will have higher possibility of getting higher income. In terms of the `stop loss`, the `sharpe ratio` are quite low for these 3 situation. However `stop_loss=-0.01` give us relative higher value which is also indicating higher guarentee of profitable. Therefore, I would pick (`p1=5`, `p2=27`, `S=1`) as the optimized set of three parameters.






# Problem 5
In practice, I think applying the best parameters generated from problem 4 directly into the real market is not wise or safe enough. Even it seems like the set of parameters that result in best performance during this time period, it might still perform badly in the future market. Therefore, I think there are at least 2 ways to better deal with such issues. 
  1. The better one and even safer one is we could gather more historical data and test out our set of parameters. This way we can generalize our model and probably find a better set of parameters that perform almost equally well on most historical data. 
  2. Another way is we could do some A/B testing first to check if such parameters is performing well for a small amount of capital. We can try out the set of parameters that has the second or third well performance with equally small amount of capital and find check result.

# Problem 6
I think we have not apply the volume column into thinking of trading. Most of time, large volume of trades in a period of time may imply an important event which is either a pretty good or bad sign for trading. But there might exists some detail implementation of such event based algorithms which I think might take time for me to get familiar with. So in summary, taking the volume into consideration of trading signal is another options.

Also, I'm considering buying or selling 1 bitcoin for each trading. I think there should exists some technique for determining the portion of shares when trading. I feel like this could be another way to respond to the market.