import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

import paper_pants.data_collection.API.oanda_api as oa

if __name__ == "__main__":
    pairs = ['EUR_USD', 'GBP_USD', 'USD_CHF', 'AUD_USD', 'USD_CAD']
    data = oa.candles('EUR_USD')
    try:
        for currency in pairs:
            data = oa.candles(currency)
            print(data)
    except:
        print("error encountered....skipping this iteration")