<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/usr/bin/env python3
"""
SHENRON INCOME MONITORING DASHBOARD
Real-time revenue tracking, customer metrics, and alerts
For LightSpeedUp Hosting - Dell R730 Passive Income System
"""

import json
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

# Configuration
DB_PATH = "C:/GOKU-AI/shenron/income_tracking.db"
STRIPE_API_KEY = "sk_test_YOUR_KEY_HERE"  # Replace with real key
PTERODACTYL_API_KEY = "ptla_YOUR_KEY_HERE"  # Replace with real key
PTERODACTYL_URL = "https://gameservers.lightspeedup.com"

class IncomeMonitor:
    def __init__(self):
        self.db_conn = sqlite3.connect(DB_PATH)
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for income tracking"""
        cursor = self.db_conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                service_type TEXT, -- game_server or wordpress
                plan TEXT,
                monthly_price REAL,
                signup_date TEXT,
                status TEXT DEFAULT 'active',
                stripe_customer_id TEXT,
                stripe_subscription_id TEXT
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                amount REAL,
                type TEXT, -- payment, refund, chargeback
                date TEXT,
                stripe_payment_id TEXT,
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Daily metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_metrics (
                date TEXT PRIMARY KEY,
                total_revenue REAL,
                new_customers INTEGER,
                churned_customers INTEGER,
                active_game_servers INTEGER,
                active_wordpress_sites INTEGER,
                expenses REAL,
                profit REAL
            )
        ''')
        
        self.db_conn.commit()
    
    def get_game_server_stats(self):
        """Get stats from Pterodactyl Panel"""
        headers = {
            "Authorization": f"Bearer {PTERODACTYL_API_KEY}",
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(
                f"{PTERODACTYL_URL}/api/application/servers",
                headers=headers
            )
            servers = response.json().get('data', [])
            
            total_servers = len(servers)
            running_servers = sum(1 for s in servers if s['attributes']['status'] == 'running')
            
            # Count by game type (from server names)
            games = {}
            for server in servers:
                name = server['attributes']['name'].lower()
                if 'minecraft' in name:
                    games['minecraft'] = games.get('minecraft', 0) + 1
                elif 'valheim' in name:
                    games['valheim'] = games.get('valheim', 0) + 1
                elif 'ark' in name:
                    games['ark'] = games.get('ark', 0) + 1
                elif 'rust' in name:
                    games['rust'] = games.get('rust', 0) + 1
                else:
                    games['other'] = games.get('other', 0) + 1
            
            return {
                'total': total_servers,
                'running': running_servers,
                'by_game': games
            }
        except Exception as e:
            print(f"Error fetching game server stats: {e}")
            return {'total': 0, 'running': 0, 'by_game': {}}
    
    def get_wordpress_stats(self):
        """Get WordPress hosting stats from VM150"""
        try:
            # SSH to VM150 and run report script
            result = subprocess.run([
                'ssh', '-i', 'C:/GOKU-AI/shenron/id_ed25519',
                'mgmt1@<VM150_IP>',
                '/root/scripts/wordpress-multi-tenant-automation.sh', 'report'
            ], capture_output=True, text=True)
            
            # Parse output
            output = result.stdout
            total_sites = 0
            revenue = 0
            
            for line in output.split('\n'):
                if 'ACTIVE SITES:' in line:
                    total_sites = int(line.split(':')[1].strip())
                elif 'TOTAL MONTHLY REVENUE:' in line:
                    revenue = float(line.split('$')[1].strip())
            
            return {
                'total_sites': total_sites,
                'monthly_revenue': revenue
            }
        except Exception as e:
            print(f"Error fetching WordPress stats: {e}")
            return {'total_sites': 0, 'monthly_revenue': 0}
    
    def get_stripe_revenue(self, days=30):
        """Get revenue from Stripe for last N days"""
        try:
            headers = {
                "Authorization": f"Bearer {STRIPE_API_KEY}"
            }
            
            # Get charges from last N days
            since = int((datetime.now() - timedelta(days=days)).timestamp())
            response = requests.get(
                "https://api.stripe.com/v1/charges",
                headers=headers,
                params={'created[gte]': since, 'limit': 100}
            )
            
            charges = response.json().get('data', [])
            
            total_revenue = sum(c['amount'] / 100 for c in charges if c['status'] == 'succeeded')
            total_refunds = sum(c['amount_refunded'] / 100 for c in charges)
            
            return {
                'total_revenue': total_revenue,
                'total_refunds': total_refunds,
                'net_revenue': total_revenue - total_refunds,
                'transaction_count': len(charges)
            }
        except Exception as e:
            print(f"Error fetching Stripe revenue: {e}")
            return {'total_revenue': 0, 'total_refunds': 0, 'net_revenue': 0, 'transaction_count': 0}
    
    def calculate_monthly_recurring_revenue(self):
        """Calculate MRR from active subscriptions"""
        cursor = self.db_conn.cursor()
        
        cursor.execute('''
            SELECT SUM(monthly_price)
            FROM customers
            WHERE status = 'active'
        ''')
        
        mrr = cursor.fetchone()[0] or 0
        return round(mrr, 2)
    
    def get_churn_rate(self, days=30):
        """Calculate customer churn rate"""
        cursor = self.db_conn.cursor()
        
        # Customers at start of period
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(*)
            FROM customers
            WHERE signup_date < ?
        ''', (start_date,))
        starting_customers = cursor.fetchone()[0]
        
        # Customers churned during period
        cursor.execute('''
            SELECT COUNT(*)
            FROM customers
            WHERE status = 'cancelled'
            AND signup_date < ?
        ''', (start_date,))
        churned = cursor.fetchone()[0]
        
        if starting_customers == 0:
            return 0
        
        churn_rate = (churned / starting_customers) * 100
        return round(churn_rate, 2)
    
    def generate_dashboard(self):
        """Generate complete income dashboard"""
        game_stats = self.get_game_server_stats()
        wp_stats = self.get_wordpress_stats()
        stripe_data = self.get_stripe_revenue(30)
        mrr = self.calculate_monthly_recurring_revenue()
        churn = self.get_churn_rate(30)
        
        # Calculate projections
        target_revenue = 3000
        progress = (mrr / target_revenue) * 100
        
        dashboard = f"""
╔══════════════════════════════════════════════════════════════╗
║          🐉 SHENRON INCOME MONITORING DASHBOARD 🐉           ║
║              LightSpeedUp Hosting - Dell R730                ║
╚══════════════════════════════════════════════════════════════╝

📊 MONTHLY RECURRING REVENUE (MRR)
═══════════════════════════════════
💰 Current MRR:    ${mrr:,.2f}
🎯 Target MRR:     $3,000.00
📈 Progress:       {progress:.1f}%
{"🔥 TARGET ACHIEVED!" if mrr >= target_revenue else f"💪 ${target_revenue - mrr:,.2f} to go!"}

🎮 GAME SERVER HOSTING
═══════════════════════
Active Servers:    {game_stats['total']}
Running Now:       {game_stats['running']}

Breakdown:
"""
        for game, count in game_stats['by_game'].items():
            dashboard += f"  • {game.title():12} {count} servers\n"
        
        dashboard += f"""
💼 WORDPRESS HOSTING
════════════════════
Active Sites:      {wp_stats['total_sites']}
Monthly Revenue:   ${wp_stats['monthly_revenue']:,.2f}

💳 STRIPE REVENUE (LAST 30 DAYS)
════════════════════════════════
Total Charges:     ${stripe_data['total_revenue']:,.2f}
Refunds:           ${stripe_data['total_refunds']:,.2f}
Net Revenue:       ${stripe_data['net_revenue']:,.2f}
Transactions:      {stripe_data['transaction_count']}

📉 CUSTOMER METRICS
═══════════════════
Churn Rate (30d):  {churn:.2f}%
Target Churn:      <15% {"✅" if churn < 15 else "⚠️"}

🎯 $3,000/MONTH GOAL BREAKDOWN
══════════════════════════════
Game Servers:      $1,200 target
WordPress:         $1,500 target
Crypto Staking:    $50 target

═══════════════════════════════════════════════════════════════
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}
═══════════════════════════════════════════════════════════════
"""
        
        return dashboard
    
    def check_alerts(self):
        """Check for alerts and anomalies"""
        alerts = []
        
        # Check MRR decline
        mrr = self.calculate_monthly_recurring_revenue()
        if mrr < 2000:  # If below 67% of goal
            alerts.append(f"⚠️ MRR is ${mrr:.2f} - below target pace")
        
        # Check churn rate
        churn = self.get_churn_rate(30)
        if churn > 15:
            alerts.append(f"🚨 High churn rate: {churn:.2f}% (target: <15%)")
        
        # Check failed payments
        stripe_data = self.get_stripe_revenue(7)  # Last week
        if stripe_data['total_refunds'] > stripe_data['total_revenue'] * 0.1:
            alerts.append(f"⚠️ High refund rate: {stripe_data['total_refunds']/stripe_data['total_revenue']*100:.1f}%")
        
        return alerts
    
    def save_daily_snapshot(self):
        """Save daily metrics to database"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        game_stats = self.get_game_server_stats()
        wp_stats = self.get_wordpress_stats()
        mrr = self.calculate_monthly_recurring_revenue()
        
        cursor = self.db_conn.cursor()
        
        # Estimate daily revenue (MRR / 30)
        daily_revenue = mrr / 30
        
        # Estimate expenses (10% of revenue for now)
        expenses = daily_revenue * 0.10
        profit = daily_revenue - expenses
        
        cursor.execute('''
            INSERT OR REPLACE INTO daily_metrics
            (date, total_revenue, new_customers, churned_customers,
             active_game_servers, active_wordpress_sites, expenses, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            today,
            daily_revenue,
            0,  # TODO: Track new customers
            0,  # TODO: Track churned customers
            game_stats['total'],
            wp_stats['total_sites'],
            expenses,
            profit
        ))
        
        self.db_conn.commit()

def main():
    """Main dashboard loop"""
    monitor = IncomeMonitor()
    
    # Generate and print dashboard
    dashboard = monitor.generate_dashboard()
    print(dashboard)
    
    # Check for alerts
    alerts = monitor.check_alerts()
    if alerts:
        print("\n🚨 ALERTS:")
        for alert in alerts:
            print(f"  {alert}")
    
    # Save daily snapshot
    monitor.save_daily_snapshot()
    print("\n✅ Daily snapshot saved to database")

if __name__ == "__main__":
    main()

