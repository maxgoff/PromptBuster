import customtkinter as ctk
from tkinter import messagebox
import asyncio
import threading
from typing import Optional
from core.workflow import PromptBusterWorkflow
from core.models import Example
from .components import ScrollableTextArea


class WorkflowTabs(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.workflow: Optional[PromptBusterWorkflow] = None
        self.setup_tabs()
    
    def setup_tabs(self):
        # Step 1: Initial Prompt Generation
        self.step1_tab = self.add("1. Initial Prompt")
        self.setup_step1()
        
        # Step 2: Examples Input
        self.step2_tab = self.add("2. Examples")
        self.setup_step2()
        
        # Step 3: Prompt Generation from Examples
        self.step3_tab = self.add("3. Generate Prompt")
        self.setup_step3()
        
        # Step 4: Evaluation Guide
        self.step4_tab = self.add("4. Eval Guide")
        self.setup_step4()
        
        # Step 5: Prompt Evaluation
        self.step5_tab = self.add("5. Evaluate")
        self.setup_step5()
        
        # Step 6: Improved Alternatives
        self.step6_tab = self.add("6. Alternatives")
        self.setup_step6()
        
        # Step 7: Final Selection
        self.step7_tab = self.add("7. Final")
        self.setup_step7()
    
    def setup_step1(self):
        frame = self.step1_tab
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame, text="Step 1: Define Role and Generate Initial Prompt Guide", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=10, sticky="w")
        
        ctk.CTkLabel(frame, text="Role (e.g., 'book authors', 'software developers'):").grid(row=1, column=0, sticky="w", pady=5)
        self.role_entry = ctk.CTkEntry(frame, placeholder_text="Enter target role...")
        self.role_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        self.generate_guide_btn = ctk.CTkButton(frame, text="Generate Prompt Guide", command=self.generate_initial_guide)
        self.generate_guide_btn.grid(row=3, column=0, pady=10)
        
        self.initial_guide_area = ScrollableTextArea(frame, height=300, placeholder="Generated prompt guide will appear here...")
        self.initial_guide_area.grid(row=4, column=0, sticky="ew", pady=10)
        
        frame.grid_rowconfigure(4, weight=1)
    
    def setup_step2(self):
        frame = self.step2_tab
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame, text="Step 2: Input 5 Examples", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=10, sticky="w")
        
        # Examples input
        self.examples_frame = ctk.CTkScrollableFrame(frame, height=500)
        self.examples_frame.grid(row=1, column=0, sticky="ew", pady=10)
        self.examples_frame.grid_columnconfigure(0, weight=1)
        
        self.example_inputs = []
        self.example_outputs = []
        
        for i in range(5):
            example_frame = ctk.CTkFrame(self.examples_frame)
            example_frame.grid(row=i, column=0, sticky="ew", pady=5)
            example_frame.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(example_frame, text=f"Example {i+1}:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
            
            ctk.CTkLabel(example_frame, text="Input:").grid(row=1, column=0, sticky="w", padx=10)
            input_entry = ctk.CTkTextbox(example_frame, height=60)
            input_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
            self.example_inputs.append(input_entry)
            
            ctk.CTkLabel(example_frame, text="Expected Output:").grid(row=3, column=0, sticky="w", padx=10)
            output_entry = ctk.CTkTextbox(example_frame, height=60)
            output_entry.grid(row=4, column=0, sticky="ew", padx=10, pady=(5, 10))
            self.example_outputs.append(output_entry)
        
        frame.grid_rowconfigure(1, weight=1)
    
    def setup_step3(self):
        frame = self.step3_tab
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame, text="Step 3: Generate Prompt from Examples", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=10, sticky="w")
        
        self.generate_prompt_btn = ctk.CTkButton(frame, text="Generate Prompt from Examples", command=self.generate_prompt_from_examples)
        self.generate_prompt_btn.grid(row=1, column=0, pady=10)
        
        self.generated_prompt_area = ScrollableTextArea(frame, height=400, placeholder="Generated prompt will appear here...")
        self.generated_prompt_area.grid(row=2, column=0, sticky="ew", pady=10)
        
        frame.grid_rowconfigure(2, weight=1)
    
    def setup_step4(self):
        frame = self.step4_tab
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame, text="Step 4: Generate Evaluation Guide", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=10, sticky="w")
        
        self.generate_eval_guide_btn = ctk.CTkButton(frame, text="Generate Evaluation Guide", command=self.generate_evaluation_guide)
        self.generate_eval_guide_btn.grid(row=1, column=0, pady=10)
        
        self.eval_guide_area = ScrollableTextArea(frame, height=400, placeholder="Evaluation guide will appear here...")
        self.eval_guide_area.grid(row=2, column=0, sticky="ew", pady=10)
        
        frame.grid_rowconfigure(2, weight=1)
    
    def setup_step5(self):
        frame = self.step5_tab
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame, text="Step 5: Evaluate the Generated Prompt", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=10, sticky="w")
        
        self.evaluate_prompt_btn = ctk.CTkButton(frame, text="Evaluate Prompt", command=self.evaluate_prompt)
        self.evaluate_prompt_btn.grid(row=1, column=0, pady=10)
        
        self.evaluation_result_area = ScrollableTextArea(frame, height=400, placeholder="Evaluation results will appear here...")
        self.evaluation_result_area.grid(row=2, column=0, sticky="ew", pady=10)
        
        frame.grid_rowconfigure(2, weight=1)
    
    def setup_step6(self):
        frame = self.step6_tab
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame, text="Step 6: Generate 3 Improved Alternatives", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=10, sticky="w")
        
        self.generate_alternatives_btn = ctk.CTkButton(frame, text="Generate Alternatives", command=self.generate_alternatives)
        self.generate_alternatives_btn.grid(row=1, column=0, pady=10)
        
        self.alternatives_area = ScrollableTextArea(frame, height=400, placeholder="Alternative prompts will appear here...")
        self.alternatives_area.grid(row=2, column=0, sticky="ew", pady=10)
        
        frame.grid_rowconfigure(2, weight=1)
    
    def setup_step7(self):
        frame = self.step7_tab
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame, text="Step 7: Select and Edit Final Prompt", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=10, sticky="w")
        
        ctk.CTkLabel(frame, text="Edit your final prompt:").grid(row=1, column=0, sticky="w", pady=5)
        
        self.final_prompt_area = ScrollableTextArea(frame, height=300, placeholder="Edit your final prompt here...")
        self.final_prompt_area.grid(row=2, column=0, sticky="ew", pady=10)
        
        self.save_final_btn = ctk.CTkButton(frame, text="Save Final Prompt", command=self.save_final_prompt)
        self.save_final_btn.grid(row=3, column=0, pady=10)
        
        frame.grid_rowconfigure(2, weight=1)
    
    def set_workflow(self, workflow: PromptBusterWorkflow):
        self.workflow = workflow
    
    def set_enabled(self, enabled: bool):
        # Enable/disable all interactive elements
        widgets_to_toggle = [
            self.role_entry, self.generate_guide_btn, self.generate_prompt_btn,
            self.generate_eval_guide_btn, self.evaluate_prompt_btn,
            self.generate_alternatives_btn, self.save_final_btn
        ]
        
        for widget in widgets_to_toggle:
            widget.configure(state="normal" if enabled else "disabled")
        
        for input_widget in self.example_inputs + self.example_outputs:
            input_widget.configure(state="normal" if enabled else "disabled")
    
    def run_async_task(self, coro, callback=None):
        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(coro)
                if callback:
                    self.after(0, lambda: callback(result))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", f"Task failed: {str(e)}"))
            finally:
                loop.close()
        
        threading.Thread(target=run_in_thread, daemon=True).start()
    
    def generate_initial_guide(self):
        if not self.workflow:
            messagebox.showerror("Error", "No workflow configured")
            return
        
        role = self.role_entry.get().strip()
        if not role:
            messagebox.showerror("Error", "Please enter a role")
            return
        
        self.workflow.set_role(role)
        self.generate_guide_btn.configure(text="Generating...", state="disabled")
        
        def on_complete(result):
            self.initial_guide_area.set_text(result)
            self.generate_guide_btn.configure(text="Generate Prompt Guide", state="normal")
        
        self.run_async_task(self.workflow.generate_initial_prompt_guide(role), on_complete)
    
    def generate_prompt_from_examples(self):
        if not self.workflow:
            messagebox.showerror("Error", "No workflow configured")
            return
        
        # Collect examples
        examples = []
        for i in range(5):
            input_text = self.example_inputs[i].get("1.0", "end-1c").strip()
            output_text = self.example_outputs[i].get("1.0", "end-1c").strip()
            
            if input_text and output_text:
                examples.append(Example(input_text=input_text, expected_output=output_text))
        
        if len(examples) < 3:
            messagebox.showerror("Error", "Please provide at least 3 complete examples")
            return
        
        role = self.workflow.session.role
        if not role:
            messagebox.showerror("Error", "Please complete Step 1 first")
            return
        
        self.generate_prompt_btn.configure(text="Generating...", state="disabled")
        
        def on_complete(result):
            self.generated_prompt_area.set_text(result)
            self.workflow.set_generated_prompt(result)
            self.generate_prompt_btn.configure(text="Generate Prompt from Examples", state="normal")
        
        self.run_async_task(self.workflow.generate_prompt_from_examples(role, examples), on_complete)
    
    def generate_evaluation_guide(self):
        if not self.workflow:
            messagebox.showerror("Error", "No workflow configured")
            return
        
        role = self.workflow.session.role
        if not role:
            messagebox.showerror("Error", "Please complete Step 1 first")
            return
        
        self.generate_eval_guide_btn.configure(text="Generating...", state="disabled")
        
        def on_complete(result):
            self.eval_guide_area.set_text(result)
            self.workflow.set_evaluation_guide(result)
            self.generate_eval_guide_btn.configure(text="Generate Evaluation Guide", state="normal")
        
        self.run_async_task(self.workflow.generate_evaluation_guide(role), on_complete)
    
    def evaluate_prompt(self):
        if not self.workflow:
            messagebox.showerror("Error", "No workflow configured")
            return
        
        if not self.workflow.session.generated_prompt:
            messagebox.showerror("Error", "Please complete Step 3 first")
            return
        
        if not self.workflow.session.evaluation_guide:
            messagebox.showerror("Error", "Please complete Step 4 first")
            return
        
        self.evaluate_prompt_btn.configure(text="Evaluating...", state="disabled")
        
        def on_complete(result):
            self.evaluation_result_area.set_text(result)
            self.workflow.set_evaluation_result(result)
            self.evaluate_prompt_btn.configure(text="Evaluate Prompt", state="normal")
        
        self.run_async_task(
            self.workflow.evaluate_prompt(
                self.workflow.session.generated_prompt,
                self.workflow.session.evaluation_guide
            ),
            on_complete
        )
    
    def generate_alternatives(self):
        if not self.workflow:
            messagebox.showerror("Error", "No workflow configured")
            return
        
        if not self.workflow.session.evaluation_result:
            messagebox.showerror("Error", "Please complete Step 5 first")
            return
        
        self.generate_alternatives_btn.configure(text="Generating...", state="disabled")
        
        def on_complete(alternatives):
            result_text = "\n\n".join([f"Alternative {i+1}:\n{alt}" for i, alt in enumerate(alternatives)])
            self.alternatives_area.set_text(result_text)
            self.workflow.set_alternative_prompts(alternatives)
            
            # Pre-populate final prompt area with the first alternative
            if alternatives:
                self.final_prompt_area.set_text(alternatives[0])
            
            self.generate_alternatives_btn.configure(text="Generate Alternatives", state="normal")
        
        self.run_async_task(
            self.workflow.generate_improved_alternatives(
                self.workflow.session.generated_prompt,
                self.workflow.session.evaluation_result
            ),
            on_complete
        )
    
    def save_final_prompt(self):
        if not self.workflow:
            messagebox.showerror("Error", "No workflow configured")
            return
        
        final_prompt = self.final_prompt_area.get_text().strip()
        if not final_prompt:
            messagebox.showerror("Error", "Please enter a final prompt")
            return
        
        self.workflow.set_final_prompt(final_prompt)
        messagebox.showinfo("Success", "Final prompt saved successfully!")
        
        # Optionally save to file or clipboard
        try:
            import pyperclip
            pyperclip.copy(final_prompt)
            messagebox.showinfo("Copied", "Final prompt copied to clipboard!")
        except ImportError:
            pass  # pyperclip not available