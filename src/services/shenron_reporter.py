"""
SHENRON Integration for ScalpStorm_V2
Real-time trade reporting and AI-powered analytics
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_settings


class ShenronReporter:
    """Report ScalpStorm activity Up SHENRON dashboard"""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        
    def report_trade(self, trade_data: Dict[str, Any]) -> bool:
        """Send trade execution data to SHENRON"""
        try:
            response = requests.post(
                f"{self.settings.shenron_url}/api/scalpstorm/trade",
                json={
                    "timestamp": datetime.utcnow().isoformat(),
                    "trade_data": trade_data,
                    "version": "2.0.0",
                    "system": "scalpstorm_v2"
                },
                timeout=5
            )
            
            if response.status_code == 200:
                self.logger.info(f"Trade reported to SHENRON: {trade_data.get('trade_id', 'unknown')}")
                return True
            else:
                self.logger.warning(f"SHENRON trade report failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"SHENRON trade report error: {e}")
            return False
    
    def report_daily_stats(self, stats: Dict[str, Any]) -> bool:
        """Send daily performance statistics to SHENRON"""
        try:
            response = requests.post(
                f"{self.settings.shenron_url}/api/scalpstorm/daily",
                json={
                    "timestamp": datetime.utcnow().isoformat(),
                    "stats": stats,
                    "version": "2.0.0"
                },
                timeout=5
            )
            if response.status_code == 200:
                self.logger.info("Daily stats reported to SHENRON")
                return True
            else:
                self.logger.warning(f"SHENRON daily stats failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"SHENRON daily stats error: {e}")
            return False
    
    def get_ai_recommendation(self, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get AI trading recommendation from SHENRON council"""
        try:
            response = requests.post(
                f"{self.settings.shenron_url}/api/scalpstorm/analyze",
                json={
                    "timestamp": datetime.utcnow().isoformat(),
                    "market_data": market_data,
                    "request_type": "trading_recommendation"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning(f"SHENRON AI recommendation failed: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"SHENRON AI recommendation error: {e}")
            return None
    
    def report_anomaly(self, anomaly_data: Dict[str, Any]) -> bool:
        """Report unusual trading patterns or anomalies"""
        try:
            response = requests.post(
                f"{self.settings.shenron_url}/api/scalpstorm/anomaly",
                json={
                    "timestamp": datetime.utcnow().isoformat(),
                    "anomaly": anomaly_data,
                    "severity": anomaly_data.get('severity', 'warning')
                },
                timeout=5
            )
            
            if response.status_code == 200:
                self.logger.warning(f"Anomaly reported to SHENRON: {anomaly_data.get('type', 'unknown')}")
                return True
            else:
                self.logger.warning(f"SHENRON anomaly report failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"SHENRON anomaly report error: {e}")
            return False
