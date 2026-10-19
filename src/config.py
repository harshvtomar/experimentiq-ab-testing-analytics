from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = 'http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv'
SOURCE_PAGE = 'https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html'
EXPECTED_SHA256 = '0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece'
EXPECTED_ROWS = 64000
COLUMNS = ['recency','history_segment','history','mens','womens','zip_code','newbie','channel','segment','visit','conversion','spend']
TREATMENTS = {'No E-Mail':'Control', 'Mens E-Mail':"Men's email", 'Womens E-Mail':"Women's email"}
ARMS = list(TREATMENTS.values())
HISTORY_BANDS = ['1) $0 - $100','2) $100 - $200','3) $200 - $350','4) $350 - $500','5) $500 - $750','6) $750 - $1,000','7) $1,000 +']
CATEGORIES = {'segment':list(TREATMENTS), 'channel':['Phone','Web','Multichannel'], 'zip_code':['Urban','Rural','Surburban','Suburban'], 'history_segment':HISTORY_BANDS}
BASELINE = ['recency','history','mens','womens','newbie']
FILTERS = ['channel','recency','history_segment','geography','newbie','mens','womens']
