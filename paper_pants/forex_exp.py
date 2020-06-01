import os
import sys
from datetime import date, datetime, timedelta, time

sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

import paper_pants.data_collection.API.oanda_api as oa
fromDate = datetime.combine(date.today(), time()) - timedelta(0,200) # 200 seconds
toDate = datetime.combine(date.today(), time())

if __name__ == "__main__":
    pairs = ['EUR_USD', 'GBP_USD', 'USD_CHF', 'AUD_USD', 'USD_CAD']
    o = oa.OandaApi(pairs)
    data = o.get_data(fromDate,toDate)
    print(data)