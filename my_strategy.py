import pandas as pd
import numpy as np
from abc import ABC, abstractclassmethod
import matplotlib.pyplot as plt


########constant#########

# Risk-free rate US: search from https://ycharts.com/indicators/1_year_treasury_bill_rate_annual
# don't know where to find the good one for such a short period, therefore assume 0
RISK_FREE_RATE = 0
# for calculating the downside variation
TARGET = 0

# plotting configuration
FIGSIZE = (100,80)
FONTSIZE = 50
BARSIZE = 1

#################

class BaseStrategy(ABC):
    @abstractclassmethod
    def generate_signal(self):
        raise NotImplementedError("Please implement the trading list method")

class SMAStrategy(BaseStrategy):

    def __init__(self, short=5, long=30, stop_loss=None, initial_capital=100000, file_path="./hist.BTCUSD.5m.csv"):
        """
        1st assumption: initial capital is 100000 USD
        """
        header = ['datetime', 'sym', 'close', 'volume']
        dtypes = {'datetime': 'str', 'sym': 'str', 'close': 'float64', 'volume': 'float64'}
        parse_dates = ['datetime']
        self.df = pd.read_csv(file_path, dtype=dtypes, parse_dates=parse_dates, index_col='datetime')
        print("Original data size: {}".format(len(self.df)))
        self._preprocess()
        print("Processed data size: {}".format(len(self.df)))
        # unit of bit coin to buy or sell when there is a signal 
        self.unit = 1
        self.long = long
        self.short = short
        self.stop_loss = stop_loss
        self.initial_capital = initial_capital
    
    def _preprocess(self):
        """
        Function to preprocess the dataframe
        """
        # 1. drop Nan value
        self.df.dropna(inplace=True)
        # 2. ascending dataframe since it is descending by date
        self.df.sort_index(inplace=True)
        # ...

    def generate_signal(self):
        self.df["ma_close_short"] = self.df['close'].rolling(window=self.short).mean()
        self.df["ma_close_long"] = self.df['close'].rolling(window=self.long).mean()
        # drop all the rows that is nan caused by rolling
        self.df.dropna(axis='index', inplace=True)
        
        if self.stop_loss:
            ix = 0
            rows = len(self.df)
            is_open = False
            self.df["signal"] = 0
            while ix < rows:
                cur_price = self.df.iloc[ix]["close"]
                if not is_open and self.df.iloc[ix]["ma_close_short"]>self.df.iloc[ix]["ma_close_long"]:
                    is_open = True
                    open_price = self.df.iloc[ix]["close"]
                    self.df.iloc[ix, 5] = 1
                elif is_open and (cur_price - open_price) / open_price < self.stop_loss:
                    is_open = False
                    open_price = cur_price
                    self.df.iloc[ix, 5] = -1
                elif is_open and self.df.iloc[ix]["ma_close_short"]<=self.df.iloc[ix]["ma_close_long"]:
                    is_open = False
                    open_price = cur_price
                    self.df.iloc[ix, 5] = -1
                ix += 1
        else:
            # this function is used to mark the position where short ma is higher then long ma
            self.df["is_buy"] = self.df.apply(lambda row: 1 if row["ma_close_short"] > row["ma_close_long"] else -1, axis='columns')

            # shift for later comparison of later condition changes
            self.df["is_buy_shift"] = self.df["is_buy"].shift(1)

            # 0 means no buy/sell happens, unit means buy unit of bitcoins, -unit means sell unit of bitcoins
            def gen_signal(row):
                if row["is_buy"]!=row["is_buy_shift"] and row["is_buy"]==1:
                    return self.unit
                elif row["is_buy"]!=row["is_buy_shift"] and row["is_buy"]==-1:
                    return -self.unit
                else:
                    return 0
            self.df["signal"] = self.df.apply(gen_signal, axis="columns")
            self.df.drop(["is_buy", "is_buy_shift"], axis="columns", inplace=True) 
        
        # check every open signal is closed
        self.df = self.__signal_validation(self.df)

    def __signal_validation(self, df):
        """
        This method will change the dataset
        """
        i = len(df) - 1
        while i >= 0 :
            if df.iloc[i]["signal"] == -1:
                return df
            # the last trading is opened but not closed
            elif df.iloc[i]["signal"] == 1:
                df.drop(df.index[i:], inplace=True)
                return df
            else:
                i-=1
        return df
    
    def generate_trading(self):
        self.df["trading"] = abs(self.df["signal"]*self.df["close"])
        # only get the close price when trading signal occurs
        trading_df = self.df.loc[self.df["trading"]!=0].copy()
        # current price: close
        # open price: forward filling the next 0 trading value with the previous not 0 value
        self.df["return_rate"] = (self.df["close"] - self.df['trading'].replace(to_replace=0, method='ffill')) / self.df['trading'].replace(to_replace=0, method='ffill')
        return trading_df

    def generate_cumpnl_curve(self, trading_df, save=True, path="cumpnl_curve.png"):
        """
        Based on the trading result, generate cumulative Profit and Loss
        for the trading_df, I only keep the record that buy/sell signal happens 

        @param trading_df: a dataframe that contains a column called trading where each row is an action of buy/sell n amount of dollar  
        """
        cumpnl = trading_df.copy()
        # just to prevent getting negative asset at the beginning
        cumpnl["cum_pnl"] = self.initial_capital
        cumpnl["cum_pnl"] = cumpnl["cum_pnl"] + (- cumpnl["signal"]*cumpnl["trading"]).cumsum(axis=0)
        # only keep rows with even index because that is the result of one round of buy and sell
        # if this line is commented out, a figure with high volitility will be generated
        cumpnl = cumpnl.iloc[1::2]

        ax = plt.gca()
        cumpnl.plot(kind='line', y='cum_pnl', color='red', ax=ax, title="short window:{}\nlong window:{}\nstop loss:{}".format(self.short, self.long, self.stop_loss))
        if save:
            assert path != None
            plt.savefig(path)
        else:
            plt.show()
        ax.clear()
        plt.close("all")
        return cumpnl

    def generate_sharpe_ratio(self):
        """
        According to the investopedia(https://www.investopedia.com/ask/answers/010815/how-do-you-calculate-sharpe-ratio-excel.asp),
        """
        # in order to let the risk free rate take effect, I use the return rate instead
        trading_df = self.df.copy()
        sharpe = (trading_df["return_rate"].mean()-RISK_FREE_RATE)/trading_df["return_rate"].std()
        print("Sharpe ratio: {}".format(sharpe))
        return sharpe
    
    def generate_sortino_ratio(self):
        """
        According to https://www.investopedia.com/terms/s/sortinoratio.asp

        Here, for the calculation of downward deviation, only negative variances are considered i.e. only those periods when the rate of return was less than the target
        """
        trading_df = self.df.copy()
        # for downside deviation, only keep the row that has less then the target value to calculate the deviation
        downside_return_rate_std = trading_df[trading_df["return_rate"]<TARGET]["return_rate"].std()
        # the rest is the same as sharpe ratio
        sortino_ratio = (trading_df["return_rate"].mean()-RISK_FREE_RATE)/downside_return_rate_std
        print("Sortino ratio: {}".format(sortino_ratio))
        return sortino_ratio
    
    def generate_maximum_drawdown(self, trading_df):
        """
        maximum drawdown is used to describe a stock's maximum high to maximum low, which indicate if a stock is profitable enough. 0% means always profit, -100% means not worth of investing 

        Here I'm using the trading df without other 0 value since the maximum drawdown is just related to the record that trade happens. Because I think the max drawdown is measuring the highest buying price and the lowest selling price. Not sure if it is accurate.
        
        @param trading_df: a dataframe that contains a column called trading where each row is an action of buy/sell n amount of dollar  
        """
        # print("Num of trading: {}".format(len(trading_df)))
        trading_df["cummax_close"] = trading_df["close"].cummax()
        # since the close - cummax_close should be negative, therefore we use cummin here
        trading_df["max_drawdown"] = ((trading_df["close"]-trading_df['cummax_close'])/trading_df["cummax_close"]).cummin()
        result = trading_df["max_drawdown"].min()
        print("maximum drawdown:{} short:{} long:{} stop_loss:{}".format(result, self.short, self.long, self.stop_loss))
        return result

    def generate_tradepnl_distribution_plot(self, trading_df, save=True, path="tradepnl_distribution.png"):
        """
        According to the PNL distribution's definition: let v[t] be the value at time t which in our case is the PNL column
        pnl_distribution = v[t+1] - v[t]

        @param trading_df: a dataframe that contains a column called trading where each row is an action of buy/sell n amount of dollar
        """
        i = 0
        trading_pnl = {"datetime":[], "pnl":[]}
        rows = len(trading_df)
        while i < rows:
            start_row = trading_df.iloc[i]
            if start_row["signal"] == 1:
                end_row = trading_df.iloc[i]
                while i<rows and end_row["signal"] != -1:
                    end_row = trading_df.iloc[i]
                    datetime = trading_df.index[i]
                    i+=1
                # to prevend the last record is buy signal
                if end_row["signal"] == -1: 
                    trading_pnl["pnl"].append(end_row["trading"] - start_row["trading"])
                    trading_pnl["datetime"].append(datetime)
            i+=1
        trading_pnl_df = pd.DataFrame({"pnl":trading_pnl["pnl"]}, index=trading_pnl["datetime"])
        ax = plt.gca()
        trading_pnl_df.plot.bar(y='pnl', color='blue', ax=ax, rot=60, figsize=FIGSIZE, fontsize=FONTSIZE, width=BARSIZE)
        if save:
            assert path is not None
            plt.savefig(path)
        else:
            plt.show()
        ax.clear()
        plt.close("all")
        return trading_pnl_df
    

def run(p1, p2, S):
    s = SMAStrategy(p1, p2, stop_loss=S)
    s.generate_signal()
    trading_df = s.generate_trading()
    s.generate_cumpnl_curve(trading_df)
    s.generate_sharpe_ratio()
    s.generate_sortino_ratio()
    s.generate_maximum_drawdown(trading_df)
    s.generate_tradepnl_distribution_plot(trading_df)


if __name__ == '__main__':
    run(5, 30, stop_loss=None)