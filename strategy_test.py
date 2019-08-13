import os
from my_strategy import SMAStrategy
header = "p1, p2, S, sharpe_ratio, sortino_ratio, max_drawdown"
FORMAT = '%(message)s'
logging.basicConfig(filename="parameters.csv", level=logging.DEBUG, format=FORMAT)
STOPLOSS = None

def traverse_parameters():
    if not os.path.isdir("figures"):
        os.mkdir("figures")

    tradepnl_template = "figures/tradepnl_distribution_{}_{}_{}.png"
    cumpnl_template = "figures/cumpnl_curve_{}_{}_{}.png"
    index_template = "{}, {}, {}, {}, {}, {}"
    for p1 in range(5, 11):
        for p2 in range(25, 31):
            s = SMAStrategy(p1, p2, stop_loss=STOPLOSS)
            s.generate_signal()
            trading_df = s.generate_trading()
            s.generate_cumpnl_curve(trading_df, save=True, path=cumpnl_template.format(p1, p2, STOPLOSS))
            sharpe = s.generate_sharpe_ratio()
            sortino = s.generate_sortino_ratio()
            max_drawdown = s.generate_maximum_drawdown(trading_df)
            info = index_template.format(p1, p2, "" if not STOPLOSS else STOPLOSS, sharpe, sortino, max_drawdown)
            logging.info(info)
            s.generate_tradepnl_distribution_plot(trading_df, save=True, path=tradepnl_template.format(p1, p2, STOPLOSS))
            del trading_df
            del s
            print()

if __name__ == '__main__':
    traverse_parameters()