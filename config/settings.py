import os
import json
from typing import Optional, Dict, Any
from pathlib import Path
from core.models import LLMConfig, LLMProvider


class SettingsManager:
    def __init__(self):
        self.config_dir = Path.home() / ".promptbuster"
        self.config_file = self.config_dir / "config.json"
        self.ensure_config_dir()
    
    def ensure_config_dir(self):
        self.config_dir.mkdir(exist_ok=True)
    
    def save_config(self, config: LLMConfig) -> None:
        """Save LLM configuration to file (excluding sensitive data)"""
        config_data = {
            "provider": config.provider.value,
            "model": config.model,
            "base_url": config.base_url,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens
        }
        
        with open(self.config_file, "w") as f:
            json.dump(config_data, f, indent=2)
    
    def load_config(self) -> Optional[LLMConfig]:
        """Load LLM configuration from file"""
        if not self.config_file.exists():
            return None
        
        try:
            with open(self.config_file, "r") as f:
                config_data = json.load(f)
            
            return LLMConfig(
                provider=LLMProvider(config_data["provider"]),
                model=config_data["model"],
                base_url=config_data.get("base_url"),
                temperature=config_data.get("temperature", 0.7),
                max_tokens=config_data.get("max_tokens", 4000)
            )
        except (json.JSONDecodeError, KeyError, ValueError):
            return None
    
    def get_api_key_from_env(self, provider: LLMProvider) -> Optional[str]:
        """Get API key from environment variables"""
        env_var_map = {
            LLMProvider.OPENAI: "OPENAI_API_KEY",
            LLMProvider.ANTHROPIC: "ANTHROPIC_API_KEY"
        }
        
        env_var = env_var_map.get(provider)
        if env_var:
            return os.getenv(env_var)
        return None
    
    def save_session(self, session_name: str, session_data: Dict[str, Any]) -> None:
        """Save a prompt engineering session"""
        sessions_dir = self.config_dir / "sessions"
        sessions_dir.mkdir(exist_ok=True)
        
        session_file = sessions_dir / f"{session_name}.json"
        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)
    
    def load_session(self, session_name: str) -> Optional[Dict[str, Any]]:
        """Load a prompt engineering session"""
        sessions_dir = self.config_dir / "sessions"
        session_file = sessions_dir / f"{session_name}.json"
        
        if not session_file.exists():
            return None
        
        try:
            with open(session_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    
    def list_sessions(self) -> list[str]:
        """List all saved sessions"""
        sessions_dir = self.config_dir / "sessions"
        if not sessions_dir.exists():
            return []
        
        return [f.stem for f in sessions_dir.glob("*.json")]