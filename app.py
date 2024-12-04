from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import ccxt

exchange = ccxt.binance({
    'options': {'defaultType': 'future'}  # Đảm bảo sử dụng thị trường Futures
})

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', methods=['GET']) 
def get_market_data(): 
    symbol = request.args.get('symbol', 'BTCUSDT') 
    data = exchange.fetch_order_book(symbol=symbol, params={'limit': 10})
    return jsonify(    data = exchange.fetch_order_book(symbol=symbol, params={'limit': 10})
) 

def background_thread(): 
    while True: 
        socketio.sleep(5) 
        data = exchange.fetch_order_book(symbol='BTCUSDT', params={'limit': 10}) 
        socketio.emit('market_data', data) 

@socketio.on('connect') 
def handle_connect(): 
    emit('message', {'data': 'Connected'}) 
    socketio.start_background_task(background_thread) 

if __name__ == '__main__': 
    socketio.run(app,host="0.0.0.0",port=5000,debug=False,allow_unsafe_werkzeug=True)

