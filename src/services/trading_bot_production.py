<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/usr/bin/env python3
"""
SHENRON-Powered Automated Crypto Trading Bot
Version: 1.0 Production
Start Capital: $100
Target: $1,578 in 6 months (20-35% monthly returns)
"""

import ccxt
import pandas as pd
import numpy as np
import time
import json
import requests
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/mgmt1/trading_bot/trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TradingBot')

class ShenronTradingBot:
    """AI-Powered Trading Bot with SHENRON Confirmation"""
    
    def __init__(self, exchange_id='binanceus', api_key='YOUR_API_KEY', 
                 api_secret='YOUR_API_SECRET', initial_capital=100):
        """
        Initialize trading bot
        
        Args:
            exchange_id: 'binanceus', 'coinbasepro', or 'kraken'
            api_key: Exchange API key (trading only, no withdrawal)
            api_secret: Exchange API secret
            initial_capital: Starting capital in USD
        """
        self.exchange_class = getattr(ccxt, exchange_id)
        self.exchange = self.exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trade_history = []
        
        # Risk management
        self.max_position_size = 0.5  # Max 50% capital per position
        self.stop_loss_pct = -1.5  # -1.5% stop loss
        self.take_profit_pct = 3.0  # 3% take profit
        self.max_daily_trades = 10
        
        # SHENRON API
        self.shenron_api = "http://<VM100_IP>:5000"
        
        logger.info(f"Trading Bot initialized with ${initial_capital}")
    
    def get_balance(self):
        """Get current USD balance"""
        try:
            balance = self.exchange.fetch_balance()
            return balance['free']['USDT'] if 'USDT' in balance['free'] else 0
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return self.capital
    
    def get_ohlcv(self, symbol='BTC/USDT', timeframe='5m', limit=100):
        """Fetch candlestick data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol}: {e}")
            return None
    
    def calculate_rsi(self, df, period=14):
        """Calculate RSI indicator"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, df):
        """Calculate MACD indicator"""
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal
    
    def calculate_indicators(self, df):
        """Calculate all technical indicators"""
        df['rsi'] = self.calculate_rsi(df)
        df['macd'], df['signal'] = self.calculate_macd(df)
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        return df
    
    def query_shenron(self, symbol, current_price, indicators, position=None):
        """
        Query SHENRON AI for trading signal
        Uses all 6 AI warriors for consensus
        """
        if position:
            entry_price = position['entry_price']
            profit_pct = (current_price - entry_price) / entry_price * 100
            query = f"""
            TRADING DECISION REQUIRED - POSITION MANAGEMENT
            
            Symbol: {symbol}
            Current Price: ${current_price:.2f}
            Entry Price: ${entry_price:.2f}
            Current Profit: {profit_pct:+.2f}%
            
            Technical Indicators:
            - RSI: {indicators['rsi']:.1f} ({'oversold' if indicators['rsi'] < 30 else 'overbought' if indicators['rsi'] > 70 else 'neutral'})
            - MACD: {indicators['macd']:.4f}
            - Signal: {indicators['signal']:.4f}
            - MACD Trend: {'bullish crossover' if indicators['macd'] > indicators['signal'] else 'bearish crossover'}
            
            Position entered {(datetime.now() - position['entry_time']).total_seconds() / 3600:.1f} hours ago.
            
            Should I:
            A) HOLD - Market conditions support holding
            B) SELL - Take profit or cut losses
            
            Provide: Decision (HOLD or SELL) and Confidence (0-100%)
            """
        else:
            query = f"""
            TRADING OPPORTUNITY ANALYSIS
            
            Symbol: {symbol}
            Current Price: ${current_price:.2f}
            
            Technical Indicators:
            - RSI: {indicators['rsi']:.1f} ({'oversold' if indicators['rsi'] < 30 else 'overbought' if indicators['rsi'] > 70 else 'neutral'})
            - MACD: {indicators['macd']:.4f} 
            - Signal: {indicators['signal']:.4f}
            - MACD vs Signal: {'MACD above signal (bullish)' if indicators['macd'] > indicators['signal'] else 'MACD below signal (bearish)'}
            - Price vs SMA20: {'Above' if current_price > indicators['sma_20'] else 'Below'} (${indicators['sma_20']:.2f})
            
            Market Setup:
            - RSI indicates: {'strong oversold - potential bounce' if indicators['rsi'] < 30 else 'strong overbought - potential reversal' if indicators['rsi'] > 70 else 'neutral zone'}
            - MACD indicates: {'bullish momentum' if indicators['macd'] > indicators['signal'] else 'bearish momentum'}
            
            Should I BUY this asset? 
            Consider: Risk/reward, momentum, trend strength.
            Provide: Decision (BUY or HOLD) and Confidence (0-100%)
            """
        
        try:
            response = requests.post(
                f"{self.shenron_api}/api/shenron/grant-wish",
                json={"query": query, "use_rag": True},
                timeout=45
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('synthesized_answer', '').upper()
                
                # Parse decision
                if 'BUY' in answer and not position:
                    decision = 'BUY'
                elif 'SELL' in answer and position:
                    decision = 'SELL'
                else:
                    decision = 'HOLD'
                
                # Extract confidence from consensus
                consensus = data.get('consensus', {})
                consensus_level = consensus.get('consensus_level', 2)
                confidence = (consensus_level / 4) * 100
                
                logger.info(f"SHENRON Decision: {decision} (Confidence: {confidence:.0f}%)")
                return decision, confidence, answer[:200]
            
            logger.warning("SHENRON API unavailable, using technical analysis only")
            return 'HOLD', 0, "SHENRON unavailable"
            
        except Exception as e:
            logger.error(f"SHENRON query failed: {e}")
            return 'HOLD', 0, "Error querying SHENRON"
    
    def should_buy(self, df, symbol):
        """Determine if we should enter a buy position"""
        latest = df.iloc[-1]
        
        # Must have positive technical signals
        technical_buy = (
            latest['rsi'] < 40 and  # Oversold or getting there
            latest['macd'] > latest['signal'] and  # MACD bullish
            latest['close'] > latest['sma_20']  # Above short-term average
        )
        
        if not technical_buy:
            return False, 0, "Technical conditions not met"
        
        # Get SHENRON confirmation
        indicators = {
            'rsi': latest['rsi'],
            'macd': latest['macd'],
            'signal': latest['signal'],
            'sma_20': latest['sma_20']
        }
        
        decision, confidence, reasoning = self.query_shenron(
            symbol, latest['close'], indicators
        )
        
        # Only buy if SHENRON confirms with >60% confidence
        should_buy = decision == 'BUY' and confidence >= 60
        
        return should_buy, confidence, reasoning
    
    def should_sell(self, df, symbol, position):
        """Determine if we should exit a position"""
        latest = df.iloc[-1]
        current_price = latest['close']
        entry_price = position['entry_price']
        
        profit_pct = (current_price - entry_price) / entry_price * 100
        
        # Automatic stop loss / take profit
        if profit_pct <= self.stop_loss_pct:
            return True, "STOP_LOSS", profit_pct, "Automatic stop loss triggered"
        
        if profit_pct >= self.take_profit_pct:
            return True, "TAKE_PROFIT", profit_pct, "Automatic take profit triggered"
        
        # Check for technical sell signals with small profit
        if profit_pct > 0.5:  # Only if we're in profit
            technical_sell = (
                latest['rsi'] > 70 or  # Overbought
                (latest['macd'] < latest['signal'] and profit_pct > 1.0)  # Bearish with profit
            )
            
            if technical_sell:
                indicators = {
                    'rsi': latest['rsi'],
                    'macd': latest['macd'],
                    'signal': latest['signal'],
                    'sma_20': latest['sma_20']
                }
                
                decision, confidence, reasoning = self.query_shenron(
                    symbol, current_price, indicators, position
                )
                
                if decision == 'SELL' and confidence >= 60:
                    return True, "AI_TECHNICAL_SELL", profit_pct, reasoning
        
        return False, "HOLD", profit_pct, "Holding position"
    
    def execute_buy(self, symbol, amount_usd):
        """Execute market buy order"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            price = ticker['last']
            amount = amount_usd / price
            
            logger.info(f"Executing BUY: {amount:.6f} {symbol} @ ${price:.2f}")
            
            # Execute order (uncomment when ready for real trading)
            # order = self.exchange.create_market_buy_order(symbol, amount)
            
            # SIMULATION MODE (comment out for real trading)
            order = {
                'symbol': symbol,
                'side': 'buy',
                'amount': amount,
                'filled': amount,
                'average': price,
                'timestamp': int(time.time() * 1000),
                'status': 'closed'
            }
            
            self.capital -= amount_usd
            logger.info(f"BUY executed. Remaining capital: ${self.capital:.2f}")
            
            return order
            
        except Exception as e:
            logger.error(f"Buy execution failed: {e}")
            return None
    
    def execute_sell(self, symbol, position):
        """Execute market sell order"""
        try:
            amount = position['amount']
            ticker = self.exchange.fetch_ticker(symbol)
            price = ticker['last']
            
            logger.info(f"Executing SELL: {amount:.6f} {symbol} @ ${price:.2f}")
            
            # Execute order (uncomment when ready for real trading)
            # order = self.exchange.create_market_sell_order(symbol, amount)
            
            # SIMULATION MODE (comment out for real trading)
            order = {
                'symbol': symbol,
                'side': 'sell',
                'amount': amount,
                'filled': amount,
                'average': price,
                'timestamp': int(time.time() * 1000),
                'status': 'closed'
            }
            
            sale_value = amount * price
            self.capital += sale_value
            logger.info(f"SELL executed. Capital now: ${self.capital:.2f}")
            
            return order
            
        except Exception as e:
            logger.error(f"Sell execution failed: {e}")
            return None
    
    def run(self, symbols=['BTC/USDT', 'ETH/USDT', 'BNB/USDT'], 
            check_interval=300):
        """
        Main trading loop
        
        Args:
            symbols: List of trading pairs
            check_interval: Seconds between checks (300 = 5 minutes)
        """
        logger.info(f"🤖 Trading Bot Started")
        logger.info(f"Initial Capital: ${self.capital:.2f}")
        logger.info(f"Symbols: {', '.join(symbols)}")
        logger.info(f"Check Interval: {check_interval}s ({check_interval/60:.0f} min)")
        logger.info("=" * 60)
        
        trades_today = 0
        last_reset = datetime.now().date()
        
        while True:
            try:
                # Reset daily trade counter
                if datetime.now().date() > last_reset:
                    trades_today = 0
                    last_reset = datetime.now().date()
                    logger.info(f"New day - trade counter reset")
                
                for symbol in symbols:
                    # Skip if max daily trades reached
                    if trades_today >= self.max_daily_trades:
                        logger.info(f"Max daily trades ({self.max_daily_trades}) reached")
                        break
                    
                    # Fetch data
                    df = self.get_ohlcv(symbol)
                    if df is None:
                        continue
                    
                    df = self.calculate_indicators(df)
                    latest = df.iloc[-1]
                    current_price = latest['close']
                    
                    # Check positions
                    if symbol not in self.positions:
                        # No position - look for buy opportunity
                        should_buy, confidence, reasoning = self.should_buy(df, symbol)
                        
                        if should_buy:
                            # Calculate position size (max 50% of capital)
                            trade_amount = min(
                                self.capital * self.max_position_size,
                                self.capital
                            )
                            
                            if trade_amount >= 10:  # Min $10 trade
                                order = self.execute_buy(symbol, trade_amount)
                                
                                if order:
                                    self.positions[symbol] = {
                                        'amount': order['filled'],
                                        'entry_price': order['average'],
                                        'entry_time': datetime.now(),
                                        'confidence': confidence
                                    }
                                    
                                    trades_today += 1
                                    
                                    logger.info("=" * 60)
                                    logger.info(f"✅ BOUGHT {symbol}")
                                    logger.info(f"   Price: ${order['average']:.2f}")
                                    logger.info(f"   Amount: {order['filled']:.6f}")
                                    logger.info(f"   Cost: ${trade_amount:.2f}")
                                    logger.info(f"   Confidence: {confidence:.0f}%")
                                    logger.info(f"   Reasoning: {reasoning[:100]}")
                                    logger.info(f"   Capital Remaining: ${self.capital:.2f}")
                                    logger.info("=" * 60)
                    
                    else:
                        # Have position - check for sell signal
                        position = self.positions[symbol]
                        should_sell, reason, profit_pct, reasoning = self.should_sell(
                            df, symbol, position
                        )
                        
                        if should_sell:
                            order = self.execute_sell(symbol, position)
                            
                            if order:
                                sale_value = order['filled'] * order['average']
                                profit = sale_value - (position['amount'] * position['entry_price'])
                                
                                # Log trade
                                self.trade_history.append({
                                    'symbol': symbol,
                                    'entry_price': position['entry_price'],
                                    'exit_price': order['average'],
                                    'profit_pct': profit_pct,
                                    'profit_usd': profit,
                                    'reason': reason,
                                    'timestamp': datetime.now()
                                })
                                
                                logger.info("=" * 60)
                                logger.info(f"💰 SOLD {symbol}")
                                logger.info(f"   Entry: ${position['entry_price']:.2f}")
                                logger.info(f"   Exit: ${order['average']:.2f}")
                                logger.info(f"   Profit: {profit_pct:+.2f}% (${profit:+.2f})")
                                logger.info(f"   Reason: {reason}")
                                logger.info(f"   Capital Now: ${self.capital:.2f}")
                                logger.info(f"   Total Gain: {(self.capital/self.initial_capital - 1)*100:+.2f}%")
                                logger.info("=" * 60)
                                
                                # Remove position
                                del self.positions[symbol]
                                trades_today += 1
                
                # Status update
                total_value = self.capital
                for sym, pos in self.positions.items():
                    try:
                        ticker = self.exchange.fetch_ticker(sym)
                        total_value += pos['amount'] * ticker['last']
                    except:
                        pass
                
                logger.info(f"\n📊 Status: Capital=${self.capital:.2f} | "
                          f"Positions={len(self.positions)} | "
                          f"Total=${total_value:.2f} | "
                          f"Gain={(total_value/self.initial_capital-1)*100:+.2f}%\n")
                
                # Sleep until next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("\n🛑 Trading bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(60)
        
        # Final summary
        logger.info("\n" + "=" * 60)
        logger.info("TRADING SESSION COMPLETE")
        logger.info(f"Initial Capital: ${self.initial_capital:.2f}")
        logger.info(f"Final Capital: ${self.capital:.2f}")
        logger.info(f"Total Gain: {(self.capital/self.initial_capital - 1)*100:+.2f}%")
        logger.info(f"Total Trades: {len(self.trade_history)}")
        logger.info("=" * 60)

# Main execution
if __name__ == '__main__':
    # CONFIGURATION
    # Replace with your actual API keys
    API_KEY = 'YOUR_BINANCE_API_KEY_HERE'
    API_SECRET = 'YOUR_BINANCE_API_SECRET_HERE'
    
    # Starting capital
    INITIAL_CAPITAL = 100
    
    # Create bot
    bot = ShenronTradingBot(
        exchange_id='binanceus',  # or 'coinbasepro', 'kraken'
        api_key=API_KEY,
        api_secret=API_SECRET,
        initial_capital=INITIAL_CAPITAL
    )
    
    # Start trading
    # Check every 5 minutes, trade BTC, ETH, BNB
    bot.run(
        symbols=['BTC/USDT', 'ETH/USDT', 'BNB/USDT'],
        check_interval=300  # 5 minutes
    )

