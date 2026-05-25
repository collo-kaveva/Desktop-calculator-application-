#!/usr/bin/env python3
"""
Modern Desktop Calculator Application
A feature-rich calculator with scientific functions, memory operations,
dark mode, and calculation history.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime


class Calculator:
    """Main calculator application class handling GUI and logic."""
    
    def __init__(self, root):
        """Initialize the calculator application."""
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Calculator state
        self.current_input = ""
        self.result = ""
        self.memory = 0
        self.history = []
        self.dark_mode = True
        
        # Color schemes
        self.colors = {
            'light': {
                'bg': '#f0f0f0',
                'display_bg': '#ffffff',
                'button_bg': '#e0e0e0',
                'button_fg': '#000000',
                'operator_bg': '#ff9500',
                'operator_fg': '#ffffff',
                'function_bg': '#a5a5a5',
                'function_fg': '#000000',
                'history_bg': '#ffffff',
                'text': '#000000'
            },
            'dark': {
                'bg': '#1c1c1c',
                'display_bg': '#2d2d2d',
                'button_bg': '#3d3d3d',
                'button_fg': '#ffffff',
                'operator_bg': '#ff9500',
                'operator_fg': '#ffffff',
                'function_bg': '#505050',
                'function_fg': '#ffffff',
                'history_bg': '#2d2d2d',
                'text': '#ffffff'
            }
        }
        
        self.setup_ui()
        self.apply_theme()
        self.setup_keyboard_bindings()
    
    def setup_ui(self):
        """Set up the user interface layout."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for display and history toggle
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Display frame
        display_frame = ttk.Frame(top_frame)
        display_frame.pack(fill=tk.X)
        
        # Expression display (shows current calculation)
        self.expression_var = tk.StringVar()
        self.expression_label = tk.Label(
            display_frame,
            textvariable=self.expression_var,
            font=('Arial', 14),
            anchor='e',
            padx=10,
            pady=5
        )
        self.expression_label.pack(fill=tk.X)
        
        # Result display
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.result_label = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 28, 'bold'),
            anchor='e',
            padx=10,
            pady=5
        )
        self.result_label.pack(fill=tk.X)
        
        # Theme toggle button
        self.theme_button = tk.Button(
            top_frame,
            text="🌙",
            font=('Arial', 16),
            command=self.toggle_theme,
            width=3,
            height=1
        )
        self.theme_button.pack(side=tk.RIGHT, pady=(5, 0))
        
        # History toggle button
        self.history_button = tk.Button(
            top_frame,
            text="📜",
            font=('Arial', 16),
            command=self.toggle_history,
            width=3,
            height=1
        )
        self.history_button.pack(side=tk.RIGHT, pady=(5, 0))
        
        # History panel (initially hidden)
        self.history_frame = ttk.Frame(main_frame)
        self.history_label = tk.Label(
            self.history_frame,
            text="Calculation History",
            font=('Arial', 12, 'bold'),
            anchor='w'
        )
        self.history_label.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        self.history_listbox = tk.Listbox(
            self.history_frame,
            font=('Arial', 10),
            height=5,
            selectmode=tk.SINGLE
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.history_listbox.bind('<Double-Button-1>', self.load_from_history)
        
        # Clear history button
        clear_history_btn = tk.Button(
            self.history_frame,
            text="Clear History",
            command=self.clear_history,
            font=('Arial', 9)
        )
        clear_history_btn.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Memory display
        self.memory_var = tk.StringVar()
        self.memory_label = tk.Label(
            top_frame,
            textvariable=self.memory_var,
            font=('Arial', 10),
            anchor='w'
        )
        self.memory_label.pack(side=tk.LEFT, pady=(5, 0))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons
        self.create_buttons(button_frame)
    
    def create_buttons(self, parent):
        """Create all calculator buttons in a grid layout."""
        button_config = [
            # Row 1: Memory functions and clear
            ['MC', 'MR', 'M+', 'M-', 'C', '⌫'],
            # Row 2: Scientific functions
            ['√', '%', '^', '(', ')', '÷'],
            # Row 3: Numbers 7-9 and multiplication
            ['7', '8', '9', '×'],
            # Row 4: Numbers 4-6 and subtraction
            ['4', '5', '6', '-'],
            # Row 5: Numbers 1-3 and addition
            ['1', '2', '3', '+'],
            # Row 6: 0, decimal, equals
            ['0', '.', '=']
        ]
        
        # Button styling
        button_width = 5
        button_height = 2
        button_font = ('Arial', 14, 'bold')
        
        for row_idx, row_buttons in enumerate(button_config):
            for col_idx, button_text in enumerate(row_buttons):
                # Determine button type for styling
                if button_text in ['+', '-', '×', '÷', '^']:
                    btn_type = 'operator'
                elif button_text in ['C', '⌫', 'MC', 'MR', 'M+', 'M-']:
                    btn_type = 'function'
                elif button_text in ['√', '%', '(', ')']:
                    btn_type = 'function'
                elif button_text == '=':
                    btn_type = 'equals'
                else:
                    btn_type = 'number'
                
                button = tk.Button(
                    parent,
                    text=button_text,
                    font=button_font,
                    width=button_width,
                    height=button_height,
                    command=lambda bt=button_text: self.on_button_click(bt)
                )
                
                # Store button type for theming
                button.btn_type = btn_type
                
                # Grid placement
                if row_idx == 0:
                    button.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky='nsew')
                elif row_idx == 1:
                    button.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky='nsew')
                elif row_idx >= 2:
                    # Adjust column for rows 2-5
                    if row_idx == 5:
                        # Last row has different layout
                        if col_idx == 0:
                            button.grid(row=row_idx, column=col_idx, columnspan=2, padx=2, pady=2, sticky='nsew')
                        else:
                            button.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky='nsew')
                    else:
                        button.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky='nsew')
                
                # Store button reference for theming
                setattr(self, f'btn_{button_text.replace("×", "x").replace("÷", "div").replace("⌫", "backspace")}', button)
        
        # Configure grid weights for responsive layout
        for i in range(6):
            parent.grid_columnconfigure(i, weight=1)
        for i in range(6):
            parent.grid_rowconfigure(i, weight=1)
    
    def apply_theme(self):
        """Apply the current theme (light or dark) to all widgets."""
        theme = self.colors['dark'] if self.dark_mode else self.colors['light']
        
        # Apply to main window
        self.root.configure(bg=theme['bg'])
        
        # Apply to display
        self.expression_label.configure(bg=theme['display_bg'], fg=theme['text'])
        self.result_label.configure(bg=theme['display_bg'], fg=theme['text'])
        self.memory_label.configure(bg=theme['bg'], fg=theme['text'])
        
        # Apply to history
        self.history_label.configure(bg=theme['bg'], fg=theme['text'])
        self.history_listbox.configure(bg=theme['history_bg'], fg=theme['text'])
        
        # Apply to buttons
        for widget in self.root.winfo_children():
            self.apply_theme_to_widget(widget, theme)
        
        # Update theme button
        self.theme_button.configure(text='☀️' if self.dark_mode else '🌙')
    
    def apply_theme_to_widget(self, widget, theme):
        """Recursively apply theme to widget and its children."""
        try:
            if isinstance(widget, tk.Button):
                if hasattr(widget, 'btn_type'):
                    btn_type = widget.btn_type
                    if btn_type == 'operator':
                        widget.configure(bg=theme['operator_bg'], fg=theme['operator_fg'])
                    elif btn_type == 'function':
                        widget.configure(bg=theme['function_bg'], fg=theme['function_fg'])
                    elif btn_type == 'equals':
                        widget.configure(bg=theme['operator_bg'], fg=theme['operator_fg'])
                    else:
                        widget.configure(bg=theme['button_bg'], fg=theme['button_fg'])
                else:
                    widget.configure(bg=theme['button_bg'], fg=theme['button_fg'])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=theme['bg'], fg=theme['text'])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=theme['bg'])
            elif isinstance(widget, ttk.Frame):
                pass  # ttk.Frame doesn't support bg directly
            
            # Recursively apply to children
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child, theme)
        except:
            pass  # Skip widgets that don't support these options
    
    def toggle_theme(self):
        """Toggle between light and dark mode."""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def toggle_history(self):
        """Show/hide the history panel."""
        if self.history_frame.winfo_ismapped():
            self.history_frame.pack_forget()
        else:
            self.history_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
    
    def on_button_click(self, button_text):
        """Handle button click events."""
        try:
            if button_text in '0123456789':
                self.append_number(button_text)
            elif button_text == '.':
                self.append_decimal()
            elif button_text in ['+', '-', '×', '÷', '^']:
                self.append_operator(button_text)
            elif button_text == '=':
                self.calculate_result()
            elif button_text == 'C':
                self.clear_all()
            elif button_text == '⌫':
                self.backspace()
            elif button_text == '√':
                self.square_root()
            elif button_text == '%':
                self.percentage()
            elif button_text in ['(', ')']:
                self.append_parenthesis(button_text)
            elif button_text == 'MC':
                self.memory_clear()
            elif button_text == 'MR':
                self.memory_recall()
            elif button_text == 'M+':
                self.memory_add()
            elif button_text == 'M-':
                self.memory_subtract()
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def append_number(self, number):
        """Append a number to the current input."""
        if self.result_var.get() == "Error" or self.result_var.get() == "0":
            self.result_var.set(number)
            self.current_input = number
        else:
            self.current_input += number
            self.result_var.set(self.current_input)
        self.update_expression_display()
    
    def append_decimal(self):
        """Append a decimal point to the current input."""
        current = self.result_var.get()
        if current == "Error":
            self.result_var.set("0.")
            self.current_input = "0."
        elif '.' not in current:
            self.current_input += '.'
            self.result_var.set(self.current_input)
        self.update_expression_display()
    
    def append_operator(self, operator):
        """Append an operator to the current input."""
        if self.current_input:
            self.current_input += f" {operator} "
            self.result_var.set(operator)
            self.update_expression_display()
    
    def append_parenthesis(self, paren):
        """Append a parenthesis to the current input."""
        self.current_input += paren
        self.result_var.set(paren)
        self.update_expression_display()
    
    def update_expression_display(self):
        """Update the expression display."""
        self.expression_var.set(self.current_input if self.current_input else "")
    
    def calculate_result(self):
        """Calculate and display the result of the current expression."""
        if not self.current_input:
            return
        
        try:
            # Prepare expression for evaluation
            expression = self.current_input
            
            # Replace display symbols with Python operators
            expression = expression.replace('×', '*').replace('÷', '/').replace('^', '**')
            
            # Evaluate the expression safely
            result = self.safe_eval(expression)
            
            # Format the result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # Add to history
            self.add_to_history(self.current_input, str(result))
            
            # Update display
            self.result_var.set(str(result))
            self.current_input = str(result)
            self.update_expression_display()
            
        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")
        except Exception as e:
            self.show_error("Invalid expression")
    
    def safe_eval(self, expression):
        """Safely evaluate a mathematical expression."""
        # Allow only mathematical characters
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars or c in '**' for c in expression):
            raise ValueError("Invalid characters in expression")
        
        # Use eval with restricted globals
        return eval(expression, {"__builtins__": None}, {})
    
    def clear_all(self):
        """Clear all input and reset the calculator."""
        self.current_input = ""
        self.result_var.set("0")
        self.expression_var.set("")
    
    def backspace(self):
        """Remove the last character from the current input."""
        if self.current_input:
            self.current_input = self.current_input[:-1].rstrip()
            if self.current_input:
                self.result_var.set(self.current_input[-1] if self.current_input[-1] in '0123456789.' else self.current_input)
            else:
                self.result_var.set("0")
            self.update_expression_display()
    
    def square_root(self):
        """Calculate the square root of the current value."""
        try:
            current = float(self.result_var.get())
            if current < 0:
                self.show_error("Invalid input")
                return
            result = math.sqrt(current)
            self.add_to_history(f"√({current})", str(result))
            self.result_var.set(str(result))
            self.current_input = str(result)
            self.update_expression_display()
        except ValueError:
            self.show_error("Invalid input")
    
    def percentage(self):
        """Calculate the percentage of the current value."""
        try:
            current = float(self.result_var.get())
            result = current / 100
            self.add_to_history(f"{current}%", str(result))
            self.result_var.set(str(result))
            self.current_input = str(result)
            self.update_expression_display()
        except ValueError:
            self.show_error("Invalid input")
    
    def memory_clear(self):
        """Clear the memory."""
        self.memory = 0
        self.update_memory_display()
    
    def memory_recall(self):
        """Recall the value from memory."""
        self.current_input += str(self.memory)
        self.result_var.set(str(self.memory))
        self.update_expression_display()
    
    def memory_add(self):
        """Add the current value to memory."""
        try:
            current = float(self.result_var.get())
            self.memory += current
            self.update_memory_display()
        except ValueError:
            pass
    
    def memory_subtract(self):
        """Subtract the current value from memory."""
        try:
            current = float(self.result_var.get())
            self.memory -= current
            self.update_memory_display()
        except ValueError:
            pass
    
    def update_memory_display(self):
        """Update the memory indicator display."""
        if self.memory != 0:
            self.memory_var.set(f"M = {self.memory}")
        else:
            self.memory_var.set("")
    
    def add_to_history(self, expression, result):
        """Add a calculation to the history."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"{timestamp} | {expression} = {result}"
        self.history.insert(0, entry)
        self.history_listbox.insert(0, entry)
        
        # Limit history to 50 entries
        if len(self.history) > 50:
            self.history.pop()
            self.history_listbox.delete(50, tk.END)
    
    def load_from_history(self, event):
        """Load a calculation from history when double-clicked."""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            entry = self.history[index]
            # Extract the result from the history entry
            result = entry.split('=')[-1].strip()
            self.current_input = result
            self.result_var.set(result)
            self.update_expression_display()
    
    def clear_history(self):
        """Clear the calculation history."""
        self.history = []
        self.history_listbox.delete(0, tk.END)
    
    def show_error(self, message):
        """Display an error message."""
        self.result_var.set("Error")
        self.current_input = ""
        self.update_expression_display()
    
    def setup_keyboard_bindings(self):
        """Set up keyboard input bindings."""
        self.root.bind('<Key>', self.handle_keypress)
    
    def handle_keypress(self, event):
        """Handle keyboard key press events."""
        key = event.char
        
        # Numbers and decimal
        if key in '0123456789.':
            self.on_button_click(key)
        # Operators
        elif key == '+':
            self.on_button_click('+')
        elif key == '-':
            self.on_button_click('-')
        elif key == '*':
            self.on_button_click('×')
        elif key == '/':
            self.on_button_click('÷')
        elif key == '^':
            self.on_button_click('^')
        # Parentheses
        elif key == '(' or key == ')':
            self.on_button_click(key)
        # Special keys
        elif event.keysym == 'Return':
            self.on_button_click('=')
        elif event.keysym == 'Escape':
            self.on_button_click('C')
        elif event.keysym == 'BackSpace':
            self.on_button_click('⌫')
        elif event.keysym == 'Delete':
            self.on_button_click('C')


def main():
    """Main function to run the calculator application."""
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
