import json
import websocket
from prettytable import PrettyTable

def rewrite(rr):
    f = open("table.txt", "w")
    f.write("\n" + rr + "\n")
    f.close()

def on_message(ws, message):
    ws.last_row_num = 0
    response = json.loads(message, encoding='utf-8')
    f = {}

    table = PrettyTable()
    table.field_names = ["SYMBOL", "ASK volume", "ASK quote", "BID volume", "BID quote"]

    for symbol in response:
        f['name'] = symbol['symbol']
#        f['ask_value'] = list(set(['{0} / {1}'.format(ask.pop('volume'), ask.pop('value'),) for ask in symbol['ask']]))
        f['ask_volume'] = list(set(['{0}'.format(ask.pop('volume'),) for ask_volume in symbol['ask_volume']]))
        f['ask_value'] = list(set(['{1}'.format(ask.pop('value'),) for ask_value in symbol['ask_value']]))
        f['bid_volume'] = list(set(['{0}'.format(bid.pop('volume'),) for bid_volume in symbol['bid_volume']]))
        f['bid_value'] = list(set(['{1}'.format(bid.pop('value'),) for bid_value in symbol['bid_value']]))
        

        for ask, bid in zip(f['ask_volume'], f['ask_value'], f['bid_volume'], f['bid_value']):
            table.add_row([f['name'], ask_volume, ask_value, '', ''])
            table.add_row([f['name'],'', '', bid_volume, bid_value])
            ws.last_row_num += 1
    print(table)
    print('\n\n')
    rewrite(str(table))

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://127.0.0.1:12001/subscribe_market_data?symbols=*&token=1@sa5",
                                on_message=on_message)
    ws.last_row_num = 0
    ws.run_forever()
