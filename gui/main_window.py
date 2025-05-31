import customtkinter as ctk
from tkinter import messagebox
import asyncio
import threading
from .workflow_tabs import WorkflowTabs
from .components import ConfigurationPanel
from core.models import LLMConfig, LLMProvider
from core.workflow import PromptBusterWorkflow


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("PromptBuster")
        self.geometry("1200x800")
        
        self.workflow = None
        self.setup_ui()
    
    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Configuration panel (left side)
        self.config_panel = ConfigurationPanel(self, self.on_config_changed)
        self.config_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # Main workflow area (right side)
        self.workflow_tabs = WorkflowTabs(self)
        self.workflow_tabs.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        
        # Initially disable workflow until configuration is set
        self.workflow_tabs.set_enabled(False)
    
    def on_config_changed(self, config: LLMConfig):
        try:
            self.workflow = PromptBusterWorkflow(config)
            self.workflow_tabs.set_workflow(self.workflow)
            self.workflow_tabs.set_enabled(True)
            messagebox.showinfo("Configuration", "LLM configuration updated successfully!")
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Failed to initialize LLM provider: {str(e)}")
            self.workflow_tabs.set_enabled(False)
    
    def run_async_task(self, coro):
        """Run async task in a separate thread to avoid blocking the GUI"""
        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(coro)
                return result
            finally:
                loop.close()
        
        return threading.Thread(target=run_in_thread, daemon=True)