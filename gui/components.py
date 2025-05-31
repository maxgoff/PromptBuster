import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Optional
from core.models import LLMConfig, LLMProvider


class ConfigurationPanel(ctk.CTkFrame):
    def __init__(self, parent, on_config_changed: Callable[[LLMConfig], None]):
        super().__init__(parent)
        self.on_config_changed = on_config_changed
        self.setup_ui()
    
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(self, text="LLM Configuration", font=ctk.CTkFont(size=16, weight="bold"))
        title.grid(row=0, column=0, pady=(10, 20), sticky="w")
        
        # Provider selection
        ctk.CTkLabel(self, text="Provider:").grid(row=1, column=0, sticky="w", pady=5)
        self.provider_var = ctk.StringVar(value="openai")
        self.provider_menu = ctk.CTkOptionMenu(
            self, 
            values=["openai", "anthropic", "local"],
            variable=self.provider_var,
            command=self.on_provider_changed
        )
        self.provider_menu.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        # Model selection
        ctk.CTkLabel(self, text="Model:").grid(row=3, column=0, sticky="w", pady=5)
        self.model_var = ctk.StringVar(value="gpt-4")
        self.model_entry = ctk.CTkEntry(self, textvariable=self.model_var)
        self.model_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        # API Key
        ctk.CTkLabel(self, text="API Key:").grid(row=5, column=0, sticky="w", pady=5)
        self.api_key_var = ctk.StringVar()
        self.api_key_entry = ctk.CTkEntry(self, textvariable=self.api_key_var, show="*")
        self.api_key_entry.grid(row=6, column=0, sticky="ew", pady=(0, 10))
        
        # Base URL (for local providers)
        ctk.CTkLabel(self, text="Base URL (optional):").grid(row=7, column=0, sticky="w", pady=5)
        self.base_url_var = ctk.StringVar()
        self.base_url_entry = ctk.CTkEntry(self, textvariable=self.base_url_var)
        self.base_url_entry.grid(row=8, column=0, sticky="ew", pady=(0, 10))
        
        # Temperature
        ctk.CTkLabel(self, text="Temperature:").grid(row=9, column=0, sticky="w", pady=5)
        self.temperature_var = ctk.StringVar(value="0.7")
        self.temperature_entry = ctk.CTkEntry(self, textvariable=self.temperature_var)
        self.temperature_entry.grid(row=10, column=0, sticky="ew", pady=(0, 10))
        
        # Max Tokens
        ctk.CTkLabel(self, text="Max Tokens:").grid(row=11, column=0, sticky="w", pady=5)
        self.max_tokens_var = ctk.StringVar(value="4000")
        self.max_tokens_entry = ctk.CTkEntry(self, textvariable=self.max_tokens_var)
        self.max_tokens_entry.grid(row=12, column=0, sticky="ew", pady=(0, 20))
        
        # Apply button
        self.apply_button = ctk.CTkButton(self, text="Apply Configuration", command=self.apply_config)
        self.apply_button.grid(row=13, column=0, sticky="ew", pady=10)
        
        self.on_provider_changed("openai")
    
    def on_provider_changed(self, provider: str):
        if provider == "openai":
            self.model_var.set("gpt-4")
            self.base_url_entry.configure(state="disabled")
        elif provider == "anthropic":
            self.model_var.set("claude-3-sonnet-20240229")
            self.base_url_entry.configure(state="disabled")
        elif provider == "local":
            self.model_var.set("local-model")
            self.base_url_entry.configure(state="normal")
            self.base_url_var.set("http://localhost:8000")
    
    def apply_config(self):
        try:
            provider = LLMProvider(self.provider_var.get())
            
            config = LLMConfig(
                provider=provider,
                model=self.model_var.get(),
                api_key=self.api_key_var.get() if self.api_key_var.get() else None,
                base_url=self.base_url_var.get() if self.base_url_var.get() else None,
                temperature=float(self.temperature_var.get()),
                max_tokens=int(self.max_tokens_var.get())
            )
            
            self.on_config_changed(config)
            
        except ValueError as e:
            messagebox.showerror("Configuration Error", f"Invalid configuration: {str(e)}")


class ScrollableTextArea(ctk.CTkFrame):
    def __init__(self, parent, height: int = 200, placeholder: str = ""):
        super().__init__(parent)
        self.setup_ui(height, placeholder)
    
    def setup_ui(self, height: int, placeholder: str):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.textbox = ctk.CTkTextbox(self, height=height)
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        if placeholder:
            self.textbox.insert("1.0", placeholder)
    
    def get_text(self) -> str:
        return self.textbox.get("1.0", "end-1c")
    
    def set_text(self, text: str):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
    
    def clear(self):
        self.textbox.delete("1.0", "end")
    
    def set_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.textbox.configure(state=state)