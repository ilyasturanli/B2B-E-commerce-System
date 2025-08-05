import tcmb


api_key = "3PE0jhSvRM"
client = tcmb.Client(api_key=api_key) # sagdaki api key üsteki api_key
usd_data = client.read(series="TP.DK.USD.S.YTL")

last_usd_data = float(usd_data.iloc[-1])


