<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
"""
ScalpStorm_V2 Configuration Settings
Production-ready configuration with environment variable support
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field, validator
import logging


class Settings(BaseSettings):
    """Main application settings loaded from environment variables."""
    
    # Exchange API Configuration
    binance_us_api_key: Optional[str] = Field(None, env="BINANCE_US_API_KEY")
    binance_us_api_secret: Optional[str] = Field(None, env="BINANCE_US_API_SECRET")
    coinex_api_key: Optional[str] = Field(None, env="COINEX_API_KEY")
    coinex_api_secret: Optional[str] = Field(None, env="COINEX_API_SECRET")
    composer_trade_api_key: Optional[str] = Field(None, env="COMPOSER_TRADE_API_KEY")
    
    # Trading Parameters
    starting_capital: float = Field(80.0, env="STARTING_CAPITAL", gt=0)
    risk_percent: float = Field(2.0, env="RISK_PERCENT", ge=0.1, le=5.0)
    max_leverage: int = Field(5, env="MAX_LEVERAGE", ge=1, le=100)
    min_profit_target: float = Field(0.003, env="MIN_PROFIT_TARGET", ge=0.001, le=0.05)
    
    # AI/ML Configuration
    model_artifact_path: Path = Field(Path("./data/models"), env="MODEL_ARTIFACT_PATH")
    training_data_path: Path = Field(Path("./data/training"), env="TRAINING_DATA_PATH")
    inference_batch_size: int = Field(32, env="INFERENCE_BATCH_SIZE", gt=0)
    
    # Risk Management
    max_position_size_usd: float = Field(1000.0, env="MAX_POSITION_SIZE_USD", gt=0)
    daily_loss_limit_percent: float = Field(10.0, env="DAILY_LOSS_LIMIT_PERCENT", ge=1, le=20)
    circuit_breaker_threshold: float = Field(0.05, env="CIRCUIT_BREAKER_THRESHOLD", ge=0, le=1)
    
    # SHENRON Integration
    shenron_url: str = Field("http://<VM100_IP>:5001", env="SHENRON_URL")
    shenron_api_key: Optional[str] = Field(None, env="SHENRON_API_KEY")
    
    # System Performance
    gpu_enabled: bool = Field(False, env="GPU_ENABLED")
    gpu_device_id: int = Field(0, env="GPU_DEVICE_ID", ge=0)
    max_workers: int = Field(4, env="MAX_WORKERS", ge=1)
    
    # Logging & Monitoring
    log_level: str = Field("INFO", env="LOG_LEVEL")
    metrics_port: int = Field(9090, env="METRICS_PORT", ge=1024, le=65535)
    health_check_port: int = Field(8081, env="HEALTH_CHECK_PORT", ge=1024, le=65535)
    
    # Operational Modes
    demo_mode: bool = Field(True, env="DEMO_MODE")
    paper_trading: bool = Field(True, env="PAPER_TRADING")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    def is_live_mode(self) -> bool:
        """Check if we're running in live trading mode."""
        return not self.demo_mode and not self.paper_trading
    
    def validate_exchange_credentials(self) -> dict:
        """Validate that required exchange credentials are present for the current mode."""
        missing = []
        
        if self.is_live_mode():
            if not self.binance_us_api_key or not self.binance_us_api_secret:
                missing.append("Binance.US")
            if not self.coinex_api_key or not self.coinex_api_secret:
                missing.append("CoinEx")
            if not self.composer_trade_api_key:
                missing.append("Composer.trade")
        
        return {
            "valid": len(missing) == 0,
            "missing_exchanges": missing
        }


def get_settings() -> Settings:
    """Get application settings with lazy loading."""
    return Settings()
