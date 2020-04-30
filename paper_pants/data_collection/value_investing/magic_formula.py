# ============================================================================
# Greenblatt's Magic Formula Implementation
# =============================================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd

class MagicFormula:
    # creating dataframe with relevant financial information for each stock using fundamental data
    stats = ["EBITDA",
            "Depreciation & amortisation",
            "Market cap (intra-day)",
            "Net income available to common shareholders",
            "Net cash provided by operating activities",
            "Capital expenditure",
            "Total current assets",
            "Total current liabilities",
            "Net property, plant and equipment",
            "Total stockholders' equity",
            "Long-term debt",
            "Forward annual dividend yield"] # change as required

    indx = ["EBITDA","D&A","MarketCap","NetIncome","CashFlowOps","Capex","CurrAsset",
            "CurrLiab","PPE","BookValue","TotDebt","DivYield"]


    def __init__(self, combined_financials):
        self.all_stats = combined_financials.loc[combined_financials.index.intersection(self.stats)]
        self.tickers = combined_financials.columns.tolist()
        self.__clean_data()

    def __clean_data(self):
        all_stats_df = pd.DataFrame(self.all_stats,index=self.indx) 
        all_stats_df = all_stats_df.replace({',': ''}, regex=True)
        all_stats_df = all_stats_df.replace({'M': 'E+03'}, regex=True)
        all_stats_df = all_stats_df.replace({'B': 'E+06'}, regex=True)
        all_stats_df = all_stats_df.replace({'T': 'E+09'}, regex=True)
        all_stats_df = all_stats_df.replace({'%': 'E-02'}, regex=True) 
        all_stats_df = all_stats_df.apply(pd.to_numeric, errors='coerce')
        all_stats_df.dropna(axis=1,inplace=True)
        self.all_stats = all_stats_df

    def __calc_relevant_metrics(self):
        transpose_df = self.all_stats.transpose()
        final_stats_df = pd.DataFrame()
        final_stats_df["EBIT"] = transpose_df["EBITDA"] - transpose_df["D&A"]
        final_stats_df["TEV"] =  transpose_df["MarketCap"].fillna(0) \
                                +transpose_df["TotDebt"].fillna(0) \
                                -(transpose_df["CurrAsset"].fillna(0)-transpose_df["CurrLiab"].fillna(0))
        final_stats_df["EarningYield"] =  final_stats_df["EBIT"]/final_stats_df["TEV"]
        final_stats_df["FCFYield"] = (transpose_df["CashFlowOps"]-transpose_df["Capex"])/transpose_df["MarketCap"]
        final_stats_df["ROC"]  = (transpose_df["EBITDA"] - transpose_df["D&A"])/(transpose_df["PPE"]+transpose_df["CurrAsset"]-transpose_df["CurrLiab"])
        final_stats_df["BookToMkt"] = transpose_df["BookValue"]/transpose_df["MarketCap"]
        final_stats_df["DivYield"] = transpose_df["DivYield"]
        self.final_stats = final_stats_df

    def print(self):                
        # finding value stocks based on Magic Formula
        final_stats_val_df = self.final_stats.loc[self.tickers,:]
        final_stats = self.final_stats
        final_stats_val_df["CombRank"] = final_stats_val_df["EarningYield"].rank(ascending=False,na_option='bottom')+final_stats_val_df["ROC"].rank(ascending=False,na_option='bottom')
        final_stats_val_df["MagicFormulaRank"] = final_stats_val_df["CombRank"].rank(method='first')
        value_stocks = final_stats_val_df.sort_values("MagicFormulaRank").iloc[:,[2,4,8]]
        print("------------------------------------------------")
        print("Value stocks based on Greenblatt's Magic Formula")
        print(value_stocks)


        # finding highest dividend yield stocks
        high_dividend_stocks = final_stats.sort_values("DivYield",ascending=False).iloc[:,6]
        print("------------------------------------------------")
        print("Highest dividend paying stocks")
        print(high_dividend_stocks)


        # # Magic Formula & Dividend yield combined
        final_stats["CombRank"] = final_stats["EarningYield"].rank(ascending=False,method='first') \
                                    +final_stats["ROC"].rank(ascending=False,method='first')  \
                                    +final_stats["DivYield"].rank(ascending=False,method='first')
        final_stats["CombinedRank"] = final_stats["CombRank"].rank(method='first')
        value_high_div_stocks = final_stats.sort_values("CombinedRank").iloc[:,[2,4,6,8]]
        print("------------------------------------------------")
        print("Magic Formula and Dividend Yield combined")
        print(value_high_div_stocks)

