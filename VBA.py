import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime
import json
import os
 
class VehicleBookingApp:
    def __init__(self, root):  # Fixed initialization method
        self.root = root
        self.root.title("Vehicle Booking Platform")
        self.root.geometry("800x700")
        
        # Set theme colors
        self.colors = {
            'primary': '#2c3e50',    # Dark blue-grey
            'secondary': '#3498db',   # Bright blue
            'accent': '#e74c3c',      # Red
            'background': '#ecf0f1',  # Light grey
            'text': '#2c3e50'         # Dark blue-grey
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'], padx=30, pady=30)
        
        # Configure styles
        self.setup_styles()

        # Variables for input fields
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.pickup_var = tk.StringVar()
        self.drop_var = tk.StringVar()
        self.ride_type = tk.StringVar(value="shared_auto")
        
        # Create and setup GUI elements
        self.setup_gui()
        
        # Load existing bookings
        self.bookings_file = "bookings.json"
        self.load_bookings()

    def setup_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')  # Use 'clam' theme as base
        
        # Configure label frame style
        style.configure(
            'Custom.TLabelframe',
            background=self.colors['background'],
            padding=15
        )
        style.configure(
            'Custom.TLabelframe.Label',
            background=self.colors['background'],
            foreground=self.colors['primary'],
            font=('Helvetica', 11, 'bold')
        )
        
        # Configure entry style
        style.configure(
            'Custom.TEntry',
            fieldbackground='white',
            padding=10
        )
        
        # Configure button styles
        style.configure(
            'Primary.TButton',
            background=self.colors['secondary'],
            foreground='white',
            padding=(20, 10),
            font=('Helvetica', 10, 'bold')
        )
        style.configure(
            'Secondary.TButton',
            background=self.colors['primary'],
            foreground='white',
            padding=(20, 10),
            font=('Helvetica', 10)
        )
        
        # Configure radio button style
        style.configure(
            'Custom.TRadiobutton',
            background=self.colors['background'],
            font=('Helvetica', 10)
        )

    def setup_gui(self):
        # Title
        title_label = ttk.Label(
            self.root,
            text="Vehicle Booking Platform",
            font=("Helvetica", 24, "bold"),
            background=self.colors['background'],
            foreground=self.colors['primary']
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # User Information Frame
        info_frame = ttk.LabelFrame(
            self.root,
            text="User Information",
            style='Custom.TLabelframe'
        )
        info_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")
        
        # Name Field
        ttk.Label(
            info_frame,
            text="Name:",
            background=self.colors['background'],
            font=('Helvetica', 10)
        ).grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(
            info_frame,
            textvariable=self.name_var,
            style='Custom.TEntry',
            width=40
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Phone Field
        ttk.Label(
            info_frame,
            text="Phone Number:",
            background=self.colors['background'],
            font=('Helvetica', 10)
        ).grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(
            info_frame,
            textvariable=self.phone_var,
            style='Custom.TEntry',
            width=40
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Location Frame
        location_frame = ttk.LabelFrame(
            self.root,
            text="Journey Details",
            style='Custom.TLabelframe'
        )
        location_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")
        
        # Pickup Location
        ttk.Label(
            location_frame,
            text="Pickup Location:",
            background=self.colors['background'],
            font=('Helvetica', 10)
        ).grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(
            location_frame,
            textvariable=self.pickup_var,
            style='Custom.TEntry',
            width=40
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Drop Location
        ttk.Label(
            location_frame,
            text="Drop Location:",
            background=self.colors['background'],
            font=('Helvetica', 10)
        ).grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(
            location_frame,
            textvariable=self.drop_var,
            style='Custom.TEntry',
            width=40
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Ride Options Frame
        ride_frame = ttk.LabelFrame(
            self.root,
            text="Ride Options",
            style='Custom.TLabelframe'
        )
        ride_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")
        
        # Radio Buttons for Ride Types
        ttk.Radiobutton(
            ride_frame,
            text="Shared Auto (₹80/km)",
            variable=self.ride_type,
            value="shared_auto",
            style='Custom.TRadiobutton'
        ).grid(row=0, column=0, padx=20, pady=10)
        
        ttk.Radiobutton(
            ride_frame,
            text="Shared Cab (₹100/km)",
            variable=self.ride_type,
            value="shared_cab",
            style='Custom.TRadiobutton'
        ).grid(row=0, column=1, padx=20, pady=10)
        
        ttk.Radiobutton(
            ride_frame,
            text="Women-Only Cab (₹120/km)",
            variable=self.ride_type,
            value="women_only_cab",
            style='Custom.TRadiobutton'
        ).grid(row=0, column=2, padx=20, pady=10)

        # Buttons Frame
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Book Button
        ttk.Button(
            button_frame,
            text="Book Ride",
            command=self.book_ride,
            style='Primary.TButton'
        ).grid(row=0, column=0, padx=10)
        
        # Clear Button
        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            style='Secondary.TButton'
        ).grid(row=0, column=1, padx=10)
        
        # View Bookings Button
        ttk.Button(
            button_frame,
            text="View Bookings",
            command=self.view_bookings,
            style='Secondary.TButton'
        ).grid(row=0, column=2, padx=10)

    def view_bookings(self):
        """Display all bookings in a new window"""
        bookings_window = tk.Toplevel(self.root)
        bookings_window.title("All Bookings")
        bookings_window.geometry("900x500")
        bookings_window.configure(bg=self.colors['background'], padx=20, pady=20)

        # Title for bookings window
        title_label = ttk.Label(
            bookings_window,
            text="Booking History",
            font=("Helvetica", 18, "bold"),
            background=self.colors['background'],
            foreground=self.colors['primary']
        )
        title_label.pack(pady=(0, 20))

        # Create Treeview with custom style
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground=self.colors['text'],
            rowheight=30,
            fieldbackground="white"
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=self.colors['primary'],
            foreground="white",
            font=('Helvetica', 10, 'bold')
        )

        columns = ('Booking ID', 'Name', 'Phone', 'Ride Type', 'Pickup', 'Drop', 'Timestamp')
        tree = ttk.Treeview(
            bookings_window,
            columns=columns,
            show='headings',
            style="Custom.Treeview"
        )
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(bookings_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert bookings with alternating row colors
        for i, booking in enumerate(self.bookings):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert('', tk.END, values=(
                booking['booking_id'],
                booking['name'],
                booking['phone'],
                booking['ride_type'].replace('_', ' ').title(),
                booking['pickup'],
                booking['drop'],
                booking['timestamp']
            ), tags=(tag,))

        # Configure row colors
        tree.tag_configure('evenrow', background='#f2f2f2')
        tree.tag_configure('oddrow', background='white')

    def validate_inputs(self):
        """Validate all input fields"""
        if not all([
            self.name_var.get().strip(),
            self.phone_var.get().strip(),
            self.pickup_var.get().strip(),
            self.drop_var.get().strip()
        ]):
            messagebox.showerror("Error", "All fields are required!")
            return False
        
        # Validate phone number (10 digits)
        if not re.match(r'^\d{10}$', self.phone_var.get().strip()):
            messagebox.showerror("Error", "Invalid phone number! Please enter 10 digits.")
            return False
            
        return True

    def book_ride(self):
        """Handle the ride booking process"""
        if not self.validate_inputs():
            return
            
        # Create booking record
        booking = {
            'booking_id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'name': self.name_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'pickup': self.pickup_var.get().strip(),
            'drop': self.drop_var.get().strip(),
            'ride_type': self.ride_type.get(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save booking
        self.bookings.append(booking)
        self.save_bookings()
        
        # Show confirmation
        messagebox.showinfo(
            "Success",
            f"Booking Confirmed!\n\nBooking ID: {booking['booking_id']}\n"
            f"Name: {booking['name']}\n"
            f"Ride Type: {booking['ride_type'].replace('_', ' ').title()}"
        )
        
        # Clear fields after successful booking
        self.clear_fields()

    def clear_fields(self):
        """Clear all input fields"""
        self.name_var.set("")
        self.phone_var.set("")
        self.pickup_var.set("")
        self.drop_var.set("")
        self.ride_type.set("shared_auto")

    def load_bookings(self):
        """Load existing bookings from file"""
        self.bookings = []
        if os.path.exists(self.bookings_file):
            try:
                with open(self.bookings_file, 'r') as f:
                    self.bookings = json.load(f)
            except json.JSONDecodeError:
                self.bookings = []

    def save_bookings(self):
        """Save bookings to file"""
        with open(self.bookings_file, 'w') as f:
            json.dump(self.bookings, f, indent=2)

def main():
    root = tk.Tk()
    app = VehicleBookingApp(root)
    root.mainloop()

if __name__ == "__main__":  # Fixed main check
    main()