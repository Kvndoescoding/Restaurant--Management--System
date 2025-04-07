import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import qrcode
import pyttsx3  
  


os.chdir("/Applications/Python 3.11")

food_menu = {
    "Burger": {"price": 150, "image": "burger.png"},
    "Pizza": {"price": 250, "image": "pizza.png"},
    "Pasta": {"price": 200, "image": "pasta.png"},
    "Fries": {"price": 100, "image": "fries.png"},
    "Coke": {"price": 50, "image": "coke.png"},
}

cart = {}

def add_to_cart(item):
    if item in cart:
        cart[item] += 1
    else:
        cart[item] = 1
    update_cart()

def update_cart():
    cart_list.delete(*cart_list.get_children())
    total = 0
    for item, quantity in cart.items():
        price = food_menu[item]["price"] * quantity
        cart_list.insert("", "end", values=(item, quantity, f"₹{price}"))
        total += price
    total_label.config(text=f"Total: ₹{total}")

def process_payment():
    total = sum(food_menu[item]["price"] * quantity for item, quantity in cart.items())
    if total == 0:
        messagebox.showerror("Error", "Cart is empty!")
        return
    
    
    payment_link = f"https://payment.com/pay?amount={total}"
    qr = qrcode.make(payment_link)
    qr_path = "payment_qr.png"
    qr.save(qr_path)

    
    img = Image.open(qr_path)
    img.show()

    
    time.sleep(10)

   
    engine = pyttsx3.init()
    engine.say("Thank you, customer")
    engine.runAndWait()

    
    cart.clear()
    update_cart()


root = tk.Tk()
root.title("Self-Ordering Restaurant System")
root.geometry("700x600")
root.configure(bg="white")

frame = tk.Frame(root, bg="white")
frame.pack(pady=20)

for item, details in food_menu.items():
    img = Image.open(details["image"])
    img = img.resize((80, 80))
    img = ImageTk.PhotoImage(img)
    btn = tk.Button(frame, text=f"{item}\n₹{details['price']}", image=img, compound="top",
                    command=lambda i=item: add_to_cart(i), bg="white")
    btn.image = img
    btn.pack(side="left", padx=10)

cart_frame = tk.Frame(root, bg="white")
cart_frame.pack(pady=20)
cart_list = ttk.Treeview(cart_frame, columns=("Item", "Quantity", "Price"), show="headings")
cart_list.heading("Item", text="Item")
cart_list.heading("Quantity", text="Quantity")
cart_list.heading("Price", text="Price")
cart_list.pack()

total_label = tk.Label(root, text="Total: ₹0", bg="white", font=("Arial", 14))
total_label.pack()

button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)
tk.Button(button_frame, text="Pay via QR", command=process_payment, bg="green", fg="white").pack(side="left", padx=10)

root.mainloop()
