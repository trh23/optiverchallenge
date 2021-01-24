from optibook.synchronous_client import Exchange

import random
import time
import datetime
import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

instrument_id_A = 'PHILIPS_A'
instrument_id_B = 'PHILIPS_B'
e = Exchange()
a = e.connect()
request_count = 0
count_start = time.time()

while 1:

    now = datetime.datetime.now()
    bookA = e.get_last_price_book(instrument_id_A)
    request_count +=1
    if request_count == 25:
        count_end = time.time()
        if count_end - count_start <= 1:
            time.sleep(1-count_end+count_start)
            request_count = 0
            count_start = time.time()
    bookB = e.get_last_price_book(instrument_id_B)
    request_count +=1
    if request_count == 25:
        count_end = time.time()
        if count_end - count_start <= 1:
            time.sleep(1-count_end+count_start)
            request_count = 0
            count_start = time.time()
    
    # find the bestBids and bestAsks and their Volume
    if len(bookA.asks) != 0 and len(bookA.bids) != 0 and len(bookB.asks) != 0 and len(bookB.bids) != 0:
        if bookA.asks[0].price <= bookB.asks[0].price:
            bestAsk = bookA.asks[0]
            bestBid = bookB.bids[0]
            marketToBuy = 'PHILIPS_A'
            marketToSell = 'PHILIPS_B'
        else:
            bestAsk = bookB.asks[0]
            bestBid = bookA.bids[0]
            marketToBuy = 'PHILIPS_B'
            marketToSell = 'PHILIPS_A'

        print("The current bestAsk: {priceA} in market {market1}, bestBid: {priceB} in market {market2}; and their volume {volumeA}, {volumeB} respectively.".format(priceA=bestAsk.price, priceB=bestBid.price, market1=marketToBuy, market2=marketToSell, volumeA=bestAsk.volume, volumeB=bestBid.volume))
        if bestBid.price > bestAsk.price:
            if bestBid.volume > bestAsk.volume:
            # bidX has a larger volume
    
            # 1st step
            # buy ask's volome (the smaller volume) and sale direcily
            # buy volume of Y and sale in X
                result = e.insert_order(marketToBuy, price = bestAsk.price, volume= bestBid.volume, side='bid', order_type='limit')
                request_count +=1
                if request_count == 25:
                    count_end = time.time()
                    if count_end - count_start <= 1:
                        time.sleep(1-count_end+count_start)
                        request_count = 0
                        count_start = time.time()

                print(f"Order Id: {result}")
                result = e.insert_order(marketToSell, price = bestBid.price, volume= bestAsk.volume, side='ask', order_type='ioc')
                request_count +=1
                if request_count == 25:
                    count_end = time.time()
                    if count_end - count_start <= 1:
                        time.sleep(1-count_end+count_start)
                        request_count = 0
                        count_start = time.time()
                print(f"Order Id: {result}")
    
    
            # 2nd step
            # use limit create an outstanding order on the Y side
            # with the price of best_ask volume of
    
            #result = e.insert_order(Y, price= best_bid.value, volume= best_bid.volume, side='ask', order_type='limit')
            #print(f"Order Id: {result}")
            else:
                result = e.insert_order(marketToBuy, price = bestAsk.price, volume= bestBid.volume, side='bid', order_type='ioc')
                request_count +=1
                if request_count == 25:
                    count_end = time.time()
                    if count_end - count_start <= 1:
                        time.sleep(1-count_end+count_start)
                        request_count = 0
                        count_start = time.time()
                print(f"Order Id: {result}")
                result = e.insert_order(marketToSell, price = bestBid.price, volume= bestAsk.volume, side='ask', order_type='limit')
                request_count +=1
                if request_count == 25:
                    count_end = time.time()
                    if count_end - count_start <= 1:
                        time.sleep(1-count_end+count_start)
                        request_count = 0
                        count_start = time.time()
                print(f"Order Id: {result}")

    # fetch lists of current outstanding orders in both A and B [list]
    OordersA = e.get_outstanding_orders(instrument_id_A)
    request_count +=1
    if request_count == 25:
        count_end = time.time()
        if count_end - count_start <= 1:
            time.sleep(1-count_end+count_start)
            request_count = 0
            count_start = time.time()
    OordersB = e.get_outstanding_orders(instrument_id_B)
    request_count +=1
    if request_count == 25:
        count_end = time.time()
        if count_end - count_start <= 1:
            time.sleep(1-count_end+count_start)
            request_count = 0
            count_start = time.time()
    print(OordersA, OordersB)

    if type(OordersA) == list:
        for order in OordersA:
            print(order)
            if order.side == 'bid':
                if order.price < bestBid.price:
                    e.amend_order(instrument_id_A, order.order_id, volume=bestBid.volume)
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
                else:
                    e.delete_order(instrument_id_A, order.order_id)
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
                    
            else:
                if order.price > bestAsk.price:
                    e.amend_order(instrument_id_A, order.order_id, volume=bestAsk.volume)
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
                else:
                    e.delete_order(instrument_id_A, order.order_id)
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
    if type(OordersB) == list:
        for order in OordersB:
            if order.side == 'bid':
                if order.price < bestBid.price:
                    e.amend_order(instrument_id_B, order.order_id, volume=bestBid.volume)
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
                else:
                    e.delete_order(instrument_id_B, order.order_id)
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
            else:
                if order.price > bestAsk.price:
                    e.amend_order(instrument_id_B, order.order_id, volume=bestAsk.volume)
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
                else:
                    e.delete_order(instrument_id_B, order.order_id)
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()

    #print(e.get_positions())
    for s, p in e.get_positions().items():
        if bookA.instrument_id == s:
            if p > 0:
                if len(bookA.asks) != 0:
                    e.insert_order(s, price=bookA.asks[0].price, volume=p, side='ask', order_type='ioc')
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
            elif p < 0:
                if len(bookA.bids) != 0:
                    e.insert_order(s, price=bookA.bids[0].price, volume=-p, side='bid', order_type='ioc')
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
                                
        else:
            if p > 0:
                if len(bookB.asks) != 0:
                    e.insert_order(s, price=bookB.asks[0].price, volume=p, side='ask', order_type='ioc')
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
            elif p < 0:
                if len(bookB.bids) != 0:
                    e.insert_order(s, price=bookB.bids[0].price, volume=-p, side='bid', order_type='ioc')
                    request_count +=1
                    if request_count == 25:
                        count_end = time.time()
                        if count_end - count_start <= 1:
                            time.sleep(1-count_end+count_start)
                            request_count = 0
                            count_start = time.time()
            
    print(e.get_positions())
    

