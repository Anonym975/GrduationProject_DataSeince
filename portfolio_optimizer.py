import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.optimize import minimize
import time
import os

# Functional Paradigm: Data downloading with retry mechanism
def download_data(tickers, start_date, end_date, retries=3, delay=5):
    for _ in range(retries):
        try:
            data = yf.download(tickers=tickers, start=start_date, end=end_date)
            if not data['Adj Close'].empty:
                return data['Adj Close']
        except Exception as e:
            print(f"Download failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    print("Failed to download data. Switching to Excel backup...")
    return None

class PortfolioOptimizer:
    def __init__(self, stocks, start, end, excel_file, target_return, riskFreeRate=0.044):
        self.stocks = stocks
        self.start = start
        self.end = end
        self.excel_file = excel_file
        self.target_return = target_return
        self.riskFreeRate = riskFreeRate

        self.prices = self.basicMetrics()
        if self.prices is not None and not self.prices.empty:
            n_assets = len(self.prices.columns)
            self.weights = np.array([1.0 / n_assets] * n_assets)
        else:
            raise ValueError("Price data is empty. Cannot initialize weights.")

        self.returns = np.log(self.prices / self.prices.shift(1)).dropna()
        self.pBar = self.returns.mean()
        self.Sigma = self.returns.cov()
        self.meanReturns, self.covMatrix = self.pBar, self.Sigma
        self.optimized_allocation = self.allocation()

    def basicMetrics(self):
        prices = download_data(self.stocks, self.start, self.end)
        if prices is None:
            try:
                prices = pd.read_excel(self.excel_file, index_col=0, parse_dates=True)
            except FileNotFoundError:
                st.error(f"❌ Excel file '{self.excel_file}' not found. Please upload it.")
                raise
        return prices

    def getData(self):
        meanReturns = self.returns.mean()
        covMatrix = self.returns.cov()
        return meanReturns, covMatrix

    def calculate_metrics(self):
        port_variance = self.portfolio_variance(self.weights, self.Sigma)
        port_annual_ret = np.sum(self.pBar * self.weights) * 252
        port_volatility = np.sqrt(port_variance)
        sharpe_ratio = (port_annual_ret - self.riskFreeRate) / port_volatility
        return port_annual_ret, port_volatility, port_variance, sharpe_ratio

    def portfolio_variance(self, weights, Sigma):
        return np.dot(weights.T, np.dot(Sigma, weights)) * 252

    def portfolioReturn(self, weights):  
        return np.sum(self.pBar * weights) * 252

    def portfolioPerformance(self, weights):
        port_annual_ret = np.sum(self.meanReturns * weights) * 252
        port_variance = self.portfolio_variance(weights, self.Sigma)
        port_volatility = np.sqrt(port_variance)
        return port_annual_ret, port_volatility

    def riskFunction(self, w):
        return self.portfolio_variance(w, self.Sigma)

    def singleEquationSolver(self):
        Sigma_inv = np.linalg.inv(self.Sigma)
        sum_all_elements = np.sum(Sigma_inv)
        w_opt = np.sum(Sigma_inv, axis=1) / sum_all_elements
        w_opt = np.maximum(w_opt, 0) / np.sum(np.maximum(w_opt, 0))
        return w_opt

    def markowitz_optimal_weights_specific_return(self, U):
        Sigma_inv = np.linalg.inv(self.Sigma)
        M = np.dot(np.dot(self.pBar.T, Sigma_inv), self.pBar)
        w_opt = np.dot(Sigma_inv, self.pBar) * (U / M)
        w_opt = np.maximum(w_opt, 0)
        return w_opt

    def allocation(self, method=None, U=None):
        if method is None:
            method = self.singleEquationSolver

        weights = method() if U is None else method(U)

        allocation_df = pd.DataFrame(
            weights,
            index=self.meanReturns.index,
            columns=["allocation"]
        )

        return allocation_df



# import yfinance as yf
# import numpy as np
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# import plotly.express as px
# from scipy.optimize import minimize
# import time
# import os

# # Functional Paradigm: Data downloading with retry mechanism
# def download_data(tickers, start_date, end_date, retries=3, delay=5):
#     for _ in range(retries):
#         try:
#             data = yf.download(tickers=tickers, start=start_date, end=end_date)
#             if not data['Adj Close'].empty:
#                 return data['Adj Close']
#         except Exception as e:
#             print(f"Download failed: {e}. Retrying in {delay} seconds...")
#             time.sleep(delay)
#     print("Failed to download data. Switching to Excel backup...")
#     return None

# class PortfolioOptimizer:
#     def __init__(self, stocks, start, end, excel_file, UserReturn, riskFreeRate=0.044):
#         self.stocks = stocks
#         self.start = start
#         self.end = end
#         self.excel_file = excel_file
#         self.UserReturn = UserReturn
#         self.riskFreeRate = riskFreeRate

#         self.prices = self.basicMetrics()
#         self.returns = np.log(self.prices / self.prices.shift(1)).dropna()
#         self.pBar = self.returns.mean()
#         self.Sigma = self.returns.cov()
#         self.weights = np.array([1.0 / len(self.prices.columns)] * len(self.prices.columns))
#         self.meanReturns, self.covMatrix = self.pBar, self.Sigma
#         self.optimized_allocation = self.allocation()

#     def basicMetrics(self):
#         prices = download_data(self.stocks, self.start, self.end)
#         if prices is None:
#             current_dir = os.path.dirname(__file__)
#             excel_path = os.path.join(current_dir, self.excel_file)
#             try:
#                 prices = pd.read_excel(excel_path, index_col=0, parse_dates=True)
#             except FileNotFoundError:
#                 raise FileNotFoundError(f"Backup Excel file not found at {excel_path}")
#         return prices

#     def getData(self):
#         # No need to call basicMetrics again; just use self.returns
#         meanReturns = self.returns.mean()
#         covMatrix = self.returns.cov()
#         return meanReturns, covMatrix

#     def calculate_metrics(self):
#         port_variance = self.portfolio_variance(self.weights, self.Sigma)
#         port_annual_ret = np.sum(self.pBar * self.weights)
#         port_volatility = np.sqrt(port_variance)
#         sharpe_ratio = (port_annual_ret - self.riskFreeRate) / port_volatility
#         return port_annual_ret, port_volatility, port_variance, sharpe_ratio

#     def portfolio_variance(self, weights, Sigma):
#         return np.dot(weights.T, np.dot(Sigma, weights))

#     def portfolioReturn(self, weights):  
#         return np.sum(self.pBar * weights)

#     def portfolioPerformance(self, weights):
#         port_annual_ret = np.sum(self.meanReturns * weights)
#         port_variance = self.portfolio_variance(weights, self.Sigma)
#         port_volatility = np.sqrt(port_variance)
#         return port_annual_ret, port_volatility

#     def riskFunction(self, w):
#         return self.portfolio_variance(w, self.Sigma)

#     def singleEquationSolver(self):
#         Sigma_inv = np.linalg.inv(self.Sigma)
#         sum_all_elements = np.sum(Sigma_inv)
#         w_opt = np.sum(Sigma_inv, axis=1) / sum_all_elements
#         w_opt = np.maximum(w_opt, 0) / np.sum(np.maximum(w_opt, 0))
#         return w_opt

#     def markowitz_optimal_weights_specific_return(self, UserReturn):
#         Sigma_inv = np.linalg.inv(self.Sigma)
#         M = np.dot(np.dot(self.pBar.T, Sigma_inv), self.pBar)
#         w_opt = np.dot(Sigma_inv, self.pBar) * (UserReturn / M)
#         w_opt = np.maximum(w_opt, 0)
#         return w_opt

#     def allocation(self):
#         optimized_allocation = pd.DataFrame(
#             self.singleEquationSolver(),
#             index=self.meanReturns.index,
#             columns=["allocation"],
#         )
#         return optimized_allocation
