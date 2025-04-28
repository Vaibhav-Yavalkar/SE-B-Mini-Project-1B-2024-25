import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import io
import base64
from src.constants import COLORS, CATEGORIES, CONDITIONS, STATES, CITIES_BY_STATE
from src.ui.modern_ui import ModernUI
import os

class DonationFormPage(ttk.Frame):
    def __init__(self, parent, submit_donation_callback, show_frame_callback):
        super().__init__(parent)
        self.parent = parent
        self.submit_donation_callback = submit_donation_callback
        self.show_frame = show_frame_callback
        self.image_data = None
        self.image_paths = []
        self.donation_entries = {}
        self.donation_state_var = tk.StringVar()
        self.donation_city_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.condition_var = tk.StringVar()
        self.state_var = tk.StringVar()
        
        # Create the main frame
        self.create_frame()
        
    def create_frame(self):
        """Create the donation form page frame"""
        # Main container with padding
        self.frame = ModernUI.create_card(self.parent)
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create a canvas with scrollbar for scrolling
        canvas = tk.Canvas(self.frame, bg=COLORS['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
        
        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=800)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            scrollable_frame,
            text="Create New Donation",
            style='Title.TLabel'
        )
        title_label.pack(pady=(20, 30))
        
        # Form container
        form_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        form_frame.pack(fill='x', padx=40)
        
        # Title field
        title_frame = ttk.Frame(form_frame, style='Card.TFrame')
        title_frame.pack(fill='x', pady=10)
        ttk.Label(title_frame, text="Title", style='Card.TLabel').pack(anchor='w')
        self.title_entry = ModernUI.create_entry(title_frame, placeholder="Enter donation title")
        self.title_entry.pack(fill='x', pady=(5,0))
        
        # Description field
        desc_frame = ttk.Frame(form_frame, style='Card.TFrame')
        desc_frame.pack(fill='x', pady=10)
        ttk.Label(desc_frame, text="Description", style='Card.TLabel').pack(anchor='w')
        self.description_text = scrolledtext.ScrolledText(
            desc_frame,
            wrap=tk.WORD,
            height=4,
            font=('Segoe UI', 10),
            bg='white',
            fg=COLORS['text']
        )
        self.description_text.pack(fill='x', pady=(5,0))
        
        # Category field
        category_frame = ttk.Frame(form_frame, style='Card.TFrame')
        category_frame.pack(fill='x', pady=10)
        ttk.Label(category_frame, text="Category", style='Card.TLabel').pack(anchor='w')
        self.category_combobox = ModernUI.create_dropdown(
            category_frame,
            CATEGORIES,
            "Select category",
            textvariable=self.category_var
        )
        self.category_combobox.pack(fill='x', pady=(5,0))
        
        # Condition field
        condition_frame = ttk.Frame(form_frame, style='Card.TFrame')
        condition_frame.pack(fill='x', pady=10)
        ttk.Label(condition_frame, text="Condition", style='Card.TLabel').pack(anchor='w')
        self.condition_combobox = ModernUI.create_dropdown(
            condition_frame,
            CONDITIONS,
            "Select condition",
            textvariable=self.condition_var
        )
        self.condition_combobox.pack(fill='x', pady=(5,0))
        
        # Location fields
        location_frame = ttk.Frame(form_frame, style='Card.TFrame')
        location_frame.pack(fill='x', pady=10)
        
        # State field
        state_frame = ttk.Frame(location_frame, style='Card.TFrame')
        state_frame.pack(fill='x')
        ttk.Label(state_frame, text="State", style='Card.TLabel').pack(anchor='w')
        self.state_combobox = ModernUI.create_dropdown(
            state_frame,
            list(STATES.keys()),
            "Select state",
            textvariable=self.state_var
        )
        self.state_combobox.pack(fill='x', pady=(5,0))
        
        # City field
        city_frame = ttk.Frame(location_frame, style='Card.TFrame')
        city_frame.pack(fill='x', pady=(10,0))
        ttk.Label(city_frame, text="City", style='Card.TLabel').pack(anchor='w')
        self.city_combobox = ModernUI.create_dropdown(
            city_frame,
            [],
            "Select city"
        )
        self.city_combobox.pack(fill='x', pady=(5,0))
        
        # Bind state selection to update cities
        self.state_var.trace('w', self.update_cities)
        
        # Image upload section
        image_frame = ttk.Frame(form_frame, style='Card.TFrame')
        image_frame.pack(fill='x', pady=20)
        ttk.Label(image_frame, text="Images", style='Card.TLabel').pack(anchor='w')
        
        # Image preview frame
        self.preview_frame = ttk.Frame(image_frame, style='Card.TFrame')
        self.preview_frame.pack(fill='x', pady=(5,10))
        
        # Upload button
        ModernUI.create_button(
            image_frame,
            "Upload Images",
            self.upload_images,
            style='Secondary.TButton'
        ).pack(anchor='w')
        
        # Button frame
        button_frame = ttk.Frame(form_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=20)
        
        # Submit button
        ModernUI.create_button(
            button_frame,
            "Submit Donation",
            self.submit_donation
        ).pack(side='left', padx=5)
        
        # Cancel button
        ModernUI.create_button(
            button_frame,
            "Cancel",
            lambda: self.show_frame('dashboard'),
            style='Secondary.TButton'
        ).pack(side='left', padx=5)
        
    def submit_donation(self):
        """Submit the donation form"""
        try:
            # Validate inputs
            title = self.title_entry.get().strip()
            description = self.description_text.get("1.0", tk.END).strip()
            category = self.category_var.get()
            condition = self.condition_var.get()
            state = self.state_var.get()
            city = self.city_combobox.get().strip()

            # Validate required fields
            if not all([title, description, category, condition, state, city]):
                messagebox.showerror("Validation Error", "Please fill in all required fields.")
                return

            # Prepare image data
            image_data = None
            image_type = None
            if self.image_paths:
                try:
                    # Read first image (can be modified to support multiple images later)
                    with open(self.image_paths[0], 'rb') as f:
                        image_data = f.read()
                    
                    # Determine image type from file extension
                    image_type = os.path.splitext(self.image_paths[0])[1][1:].lower()  # e.g., 'png', 'jpg'
                except (IOError, IndexError) as e:
                    messagebox.showerror("Image Error", f"Failed to process image: {str(e)}")
                    return

            # Submit donation
            success = self.submit_donation_callback(
                title=title,
                description=description,
                category=category,
                condition=condition,
                state=state,
                city=city,
                image_data=image_data,
                image_type=image_type
            )
            
            if success:
                # Clear form
                self.title_entry.delete(0, tk.END)
                self.description_text.delete('1.0', tk.END)
                self.category_var.set('')
                self.condition_var.set('')
                self.state_var.set('')
                self.city_combobox.set("")
                # Clear image paths and previews
                self.image_paths = []
                for widget in self.preview_frame.winfo_children():
                    widget.destroy()
                # Redirect to dashboard
                self.show_frame('DashboardPage')

        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred: {str(e)}")
    
    def update_char_counter(self, widget, counter_label, max_chars, is_text=False):
        """Update character counter for text inputs"""
        if is_text:
            current_chars = len(widget.get('1.0', 'end-1c'))
        else:
            current_chars = len(widget.get())
        counter_label.config(text=f"{current_chars}/{max_chars}")
        
        # Visual feedback when approaching/exceeding limit
        if current_chars > max_chars:
            counter_label.config(foreground='red')
        elif current_chars > max_chars * 0.9:  # 90% of limit
            counter_label.config(foreground='orange')
        else:
            counter_label.config(foreground='black')

    def clear_form(self):
        # Clear all form fields
        self.title_entry.delete(0, 'end')
        self.description_text.delete('1.0', 'end')
        self.category_var.set("Select category")
        self.condition_var.set("Select condition")
        self.state_var.set("Select state")
        self.city_combobox.set("Select city")
        # Clear image paths and previews
        self.image_paths = []
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
    def preview_donation(self):
        """Show a preview of the donation before submitting"""
        # Validate required fields
        title = self.title_entry.get()
        description = self.description_text.get('1.0', 'end-1c')
        category = self.category_combobox.get()
        condition = self.condition_combobox.get()
        location = f"{self.city_combobox.get()}, {self.state_combobox.get()}"
        
        if not all([title, description, category, condition, location]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        # Create preview window
        preview = tk.Toplevel(self)
        preview.title("Preview Donation")
        preview.geometry("800x600")
        preview.configure(bg=COLORS['background'])
        preview.transient(self)
        preview.grab_set()
        
        # Create main container
        main_frame = ttk.Frame(preview, style='Card.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left side - Image preview
        image_frame = ttk.Frame(main_frame, style='Card.TFrame')
        image_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Image display with shadow effect
        image_label = ttk.Label(image_frame, style='Card.TLabel')
        image_label.pack(fill='both', expand=True, padx=10, pady=10)
        
        if self.image_paths:
            try:
                img = Image.open(self.image_paths[0])
                img.thumbnail((400, 400))  # Maintain aspect ratio
                photo = ImageTk.PhotoImage(img)
                image_label.configure(image=photo)
                image_label.image = photo
            except:
                image_label.configure(text="Error loading image")
        else:
            image_label.configure(text="No image selected")
        
        # Right side - Details preview
        details_frame = ttk.Frame(main_frame, style='Card.TFrame')
        details_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Title
        title_label = ttk.Label(
            details_frame,
            text=title,
            font=('Segoe UI', 24, 'bold'),
            foreground=COLORS['primary'],
            style='Card.TLabel',
            wraplength=350
        )
        title_label.pack(fill='x', pady=(0, 10))
        
        # Category and condition badges
        badge_frame = ttk.Frame(details_frame, style='Card.TFrame')
        badge_frame.pack(fill='x', pady=(0, 15))
        
        category_label = ttk.Label(
            badge_frame,
            text=category,
            style='CategoryBadge.TLabel'
        )
        category_label.pack(side='left', padx=(0, 5))
        
        condition_label = ttk.Label(
            badge_frame,
            text=condition,
            style='ConditionBadge.TLabel'
        )
        condition_label.pack(side='left')
        
        # Description
        desc_label = ttk.Label(
            details_frame,
            text="Description",
            font=('Segoe UI', 12, 'bold'),
            style='Card.TLabel'
        )
        desc_label.pack(fill='x', pady=(0, 5))
        
        desc_text = tk.Text(
            details_frame,
            wrap=tk.WORD,
            height=6,
            font=('Segoe UI', 10),
            bg=COLORS['card'],
            fg=COLORS['text']
        )
        desc_text.insert('1.0', description)
        desc_text.configure(state='disabled')
        desc_text.pack(fill='both', expand=True, pady=(0, 15))
        
        # Location info
        info_frame = ttk.Frame(details_frame, style='Card.TFrame')
        info_frame.pack(fill='x', pady=(0, 15))
        
        location_frame = ttk.Frame(info_frame, style='Card.TFrame')
        location_frame.pack(fill='x', pady=2)
        ttk.Label(
            location_frame,
            text="",
            style='Card.TLabel'
        ).pack(side='left')
        ttk.Label(
            location_frame,
            text=location,
            style='Card.TLabel'
        ).pack(side='left', padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(details_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(15, 0))
        
        ModernUI.create_button(
            button_frame,
            "Submit Donation",
            lambda: [self.submit_donation(), preview.destroy()],
            width=20
        ).pack(side='left', padx=5)
        
        ModernUI.create_button(
            button_frame,
            "Edit",
            preview.destroy,
            style='Secondary.TButton',
            width=15
        ).pack(side='right', padx=5)
    
    def upload_images(self):
        # Open file dialog to select image
        file_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")],
            multiple=True
        )
        
        if not file_paths:
            return
            
        # Add selected images to the list
        for file_path in file_paths:
            if file_path not in self.image_paths:
                self.image_paths.append(file_path)
                self._add_image_preview(file_path)
                
        # Update the preview frame
        self.preview_frame.update()
    
    def _add_image_preview(self, file_path):
        try:
            # Create a thumbnail of the image
            image = Image.open(file_path)
            image.thumbnail((100, 100))  # Resize to thumbnail
            photo = ImageTk.PhotoImage(image)
            
            # Create a frame for the image preview
            img_preview_frame = ttk.Frame(self.preview_frame, style='Card.TFrame')
            img_preview_frame.pack(side='left', padx=5, pady=5)
            
            # Create a label to display the image
            preview_label = ttk.Label(img_preview_frame, image=photo)
            preview_label.image = photo  # Keep a reference
            preview_label.pack(padx=5, pady=5)
            
            # Create a remove button
            remove_btn = ttk.Button(
                img_preview_frame, 
                text="", 
                width=2,
                command=lambda fp=file_path, frame=img_preview_frame: self._remove_image(fp, frame)
            )
            remove_btn.pack(pady=(0, 5))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def _remove_image(self, file_path, frame):
        # Remove the image from the list
        if file_path in self.image_paths:
            self.image_paths.remove(file_path)
        
        # Remove the preview from the UI
        frame.destroy()
        
    def update_cities(self, *args):
        state = self.state_var.get()
        if state in CITIES_BY_STATE:
            self.city_combobox['values'] = CITIES_BY_STATE[state]
            self.city_combobox.set("Select city")
        else:
            self.city_combobox['values'] = []
            self.city_combobox.set("")