from optibook.synchronous_client import Exchange

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

instrument_id = 'PHILIPS_A'

e = Exchange()
a = e.connect()

# you can also define host/user/pass yourself
# when not defined, it is taken from ~/.optibook file if it exists
# if that file does not exists, an error is thrown

#e = Exchange(host='host-to-connect-to')
#a = e.connect(username='your-username', password='your-password')

# Returns all currently outstanding orders
orders = e.get_outstanding_orders(instrument_id)
for o in orders.values():
    print('outstanding orders: ' + o)
    
# Returns all trades you have done since the last time this function was called
trades = e.poll_new_trades(instrument_id)
for t in trades:
    print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
    
# Returns all trades you have done since since the instantiation of the Exchange
trades = e.get_trade_history(instrument_id)
for t in trades:
    print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")

# Returns all current positions
positions = e.get_positions()
for p in positions:
    print(p, positions[p])
    
# Returns all current positions with cash investedx
positions = e.get_positions_and_cash()
for p in positions:
    print(p, positions[p])
    
# Returns Current PnL based on last Traded Price
pnl = e.get_pnl()
print(pnl)

book_A = e.get_last_price_book("PHILIPS_A")
book_B = e.get_last_price_book("PHILIPS_B")
print('bids_PHILIPS_A:')
print("bid\tprice\task")
for i in reversed(book_A.asks):
  print('\t'+str(round(i.price,1))+'\t'+str(i.volume))
for i in book_A.bids:
    print(str(i.volume)+'\t'+str(round(i.price,1))+'\t')


# Returns all public tradeticks since the last time this function was called
tradeticks = e.poll_new_trade_ticks(instrument_id)
for t in tradeticks:
    print(f"[{t.instrument_id}] price({t.price}), volume({t.volume}), aggressor_side({t.aggressor_side}), buyer({t.buyer}), seller({t.seller})")
    
# Returns all public tradeticks since the instantiation of the Exchange
tradeticks = e.get_trade_tick_history(instrument_id)
for t in tradeticks:
    print(t)
    
# See all your outstanding orders
outstanding = e.get_outstanding_orders(instrument_id)
for o in outstanding.values():
    print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")

#result = e.insert_order(instrument_id, price=78.9, volume=1, side='bid', order_type='limit')
