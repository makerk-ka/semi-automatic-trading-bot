#import packages
import binance.client 
from binance.client import Client 
import pandas as pd 

#pass Public and Secret Key
Pkey = 'Your ApiKey' 
Skey = 'Your SecretKey'

#Create an instance of Client
client = Client(api_key=Pkey, api_secret=Skey)

def format_value(valuetoformatx,fractionfactorx):
					value = valuetoformatx
					fractionfactor = fractionfactorx
					Precision = abs(int(f'{fractionfactor:e}'.split('e')[-1]))
					FormattedValue = float('{:0.0{}f}'.format(value, Precision))
					return FormattedValue		
 
def pairPriceinfo(ticker,client): 
				info = client.get_symbol_info(ticker)
				minPrice = pd.to_numeric(info['filters'][0]['minPrice'])  #  0 to isolate  price precision   #  2 to isloate qty 
				return minPrice

def pairQtyinfo(ticker,client):
					info = client.get_symbol_info(ticker)
					minQty = pd.to_numeric(info['filters'][2]['minQty'])   
					#print()
					return minQty 
					
#Function to get out total balance
def Get_Free_balance(asset):
	jsonBalance = client.get_asset_balance(asset=asset)
	freeBalance = float(jsonBalance['free'])
	return freeBalance


#Function to place Market buy order ***USDT
def Market_buy_order(ticker, float(ptcUse)):

	#Create asset
	asset = ticker[:-4].upper()
	pctUse = pctUse/100
	
 	#Get the avg ticker price
	price = client.get_avg_price(symbol=ticker)
	price = float(price['price'])
	
	#Calculate the quantity that we will buy
	freeBalance = Get_Free_balance(asset)
	BalanceToUse = freeBalance*pctUse
	qty = BalanceToUse/price
	#Format quantity
	minQty = pairQtyinfo(ticker,client)
	qtyFormatted = format_value(qty,minQty)
	#Excute buy order
	order = client.order_market_buy(symbol = ticker, quantity = qtyFormatted)
	print('\n Market BuyOrder is 100/100 Executed')
	
#Function to place OCO order ***USDT
def OCO_order(ticker, float(pct_tp), float(pct_sl)):

	#Create asset
	asset = ticker[:-4].upper()
	
	#Get the free asset balance 
	assetBalance = client.get_asset_balance(asset = asset)
	assetBalance = float(assetBalance['free'])
	
	#Calculate the quantity that we will sell & Format quantity
	minQty = pairQtyinfo(ticker,client)
	assetBalance = format_value(assetBalance,minQty)
	
	#limit price , stopPrice , stopLimit.
	#take profit
	pct_tp = pct_tp/100
	#stop loss
	pct_sl = pct_sl/100
	
	#Get current price
	price = client.get_avg_price(symbol=ticker)
	price = float(price['price'])

	#Calculate & Format TP
	minPrice = pairPriceinfo(ticker,client)
	Above = price+(price*pct_tp)
	Above = format_value(Above,minPrice)
	#Calculate & Format Trigger
	belowTrigger = price-(price*pct_sl)
	belowTrigger = format_value(belowTrigger,minPrice)
	#Calculate & Format SL
	belowLimit = belowTrigger-(belowTrigger*0.001)
	belowLimit = format_value(belowLimit,minPrice)
	
	#place oco order
	orderoco = client.create_oco_order(symbol= ticker,side ='SELL',
						quantity= assetBalance,
								price = Above ,
									stopPrice= belowTrigger, 
										stopLimitPrice = belowLimit,
											limitIcebergQty =0,
												stopIcebergQty = 0,																	
													stopLimitTimeInForce= 'GTC')
	print('\n OCO Order is 100/100 Executed')
	
#Function to place Market sell order ***USDT
def Market_sell_order(ticker):
	
	#Create asset
	asset = ticker[:-4].upper()
	#Get the free asset balance
	freeBalance = Get_Free_balance(asset)
	#Format quantity
	minQty = pairQtyinfo(ticker,client) 
	freeBalance = format_value(freeBalance,minQty)
	#Place market sell order
	order = client.order_market_sell(symbol = ticker, quantity = qty)
	print('\n Market Sell Order is 100/100 Executed')

	 
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	

