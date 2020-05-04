# ============================================================================
# Piotroski f score implementation  
# =============================================================================

import pandas as pd

class PiotroskiFScore:
    stats = [fig.lower().strip() for fig in ["Net income available to common shareholders",
         "Total assets",
         "Net cash provided by operating activities",
         "Long-term debt",
         "Other long-term liabilities",
         "Total current assets",
         "Total current liabilities",
         "Common stock",
         "Total revenue",
         "Gross profit"]] # change as required

    indx = ["NetIncome","TotAssets","CashFlowOps","LTDebt","OtherLTDebt",
        "CurrAssets","CurrLiab","CommStock","TotRevenue","GrossProfit"]
    
    def __init__(self, combined_financials):
        self.all_figures = combined_financials.loc[combined_financials.index.intersection(self.stats)] 

        rename_fig_dict = {self.stats[i]: self.indx[i] for i in range(len(self.stats))}

        self.all_figures = self.all_figures.rename(index=rename_fig_dict)
        self.__clean_data()
        self.__piotroski_f()

    def __clean_data(self):
        """
            drop stocks with nan values so we only have stocks that we can use
        """
        
        self.all_figures.dropna(axis=1,inplace=True)        
        self.tickers =  set([company[0] for company in self.all_figures.columns.tolist()]) # make list unique
       
    def __piotroski_f(self):
        """
        function to calculate f score of each stock and output information as dataframe
        """
        f_score = {}
        tickers = self.tickers
        df = self.all_figures
        for ticker in tickers:
            ROA_FS = int(df.loc["NetIncome",ticker][0]/((df.loc["TotAssets",ticker][0]+df.loc["TotAssets",ticker][1])/2) > 0)
            CFO_FS = int(df.loc["CashFlowOps",ticker][0] > 0)
            ROA_D_FS = int(df.loc["NetIncome",ticker][0]/(df.loc["TotAssets",ticker][0]+df.loc["TotAssets",ticker][1])/2 > df.loc["NetIncome",ticker][1]/(df.loc["TotAssets",ticker][1]+df.loc["TotAssets",ticker][2])/2)
            CFO_ROA_FS = int(df.loc["CashFlowOps",ticker][0]/df.loc["TotAssets",ticker][0] > df.loc["NetIncome",ticker][0]/((df.loc["TotAssets",ticker][0]+df.loc["TotAssets",ticker][1])/2))
            LTD_FS = int((df.loc["LTDebt",ticker][0] + df.loc["OtherLTDebt",ticker][0])<(df.loc["LTDebt",ticker][1] + df.loc["OtherLTDebt",ticker][1]))
            CR_FS = int((df.loc["CurrAssets",ticker][0]/df.loc["CurrLiab",ticker][0])>(df.loc["CurrAssets",ticker][1]/df.loc["CurrLiab",ticker][1]))
            DILUTION_FS = int(df.loc["CommStock",ticker][0] <= df.loc["CommStock",ticker][1])
            GM_FS = int((df.loc["GrossProfit",ticker][0]/df.loc["TotRevenue",ticker][0])>(df.loc["GrossProfit",ticker][1]/df.loc["TotRevenue",ticker][1]))
            ATO_FS = int(df.loc["TotRevenue",ticker][0]/((df.loc["TotAssets",ticker][0]+df.loc["TotAssets",ticker][1])/2)>df.loc["TotRevenue",ticker][1]/((df.loc["TotAssets",ticker][1]+df.loc["TotAssets",ticker][2])/2))
            f_score[ticker] = [ROA_FS,CFO_FS,ROA_D_FS,CFO_ROA_FS,LTD_FS,CR_FS,DILUTION_FS,GM_FS,ATO_FS]
        f_score_df = pd.DataFrame(f_score,index=["PosROA","PosCFO","ROAChange","Accruals","Leverage","Liquidity","Dilution","GM","ATO"])
        self.f_score_df = f_score_df.sum().sort_values(ascending=False)
        
    def print(self):
        print(self.f_score_df)