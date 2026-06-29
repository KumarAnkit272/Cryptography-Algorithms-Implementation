import tkinter as tk
from tkinter import messagebox, scrolledtext
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64

# =========================
# Functions
# =========================

current_key = None

def generate_key():
    global current_key

    current_key = get_random_bytes(16)

    key_entry.delete(0, tk.END)
    key_entry.insert(0, current_key.hex())

    messagebox.showinfo(
        "Success",
        "AES-128 Key Generated Successfully!"
    )


def aes_encrypt():
    try:
        text = input_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning(
                "Warning",
                "Enter text first!"
            )
            return

        key_hex = key_entry.get().strip()

        if len(key_hex) != 32:
            messagebox.showerror(
                "Error",
                "AES-128 key must be 32 hex characters."
            )
            return

        key = bytes.fromhex(key_hex)

        cipher = AES.new(key, AES.MODE_CBC)

        encrypted = cipher.encrypt(
            pad(text.encode(), AES.block_size)
        )

        result = base64.b64encode(
            cipher.iv + encrypted
        ).decode()

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def aes_decrypt():
    try:
        encrypted_data = output_text.get(
            "1.0",
            tk.END
        ).strip()

        key_hex = key_entry.get().strip()

        key = bytes.fromhex(key_hex)

        raw = base64.b64decode(encrypted_data)

        iv = raw[:16]
        ciphertext = raw[16:]

        cipher = AES.new(
            key,
            AES.MODE_CBC,
            iv
        )

        decrypted = unpad(
            cipher.decrypt(ciphertext),
            AES.block_size
        )

        input_text.delete("1.0", tk.END)
        input_text.insert(
            tk.END,
            decrypted.decode()
        )

        messagebox.showinfo(
            "Success",
            "Decryption Successful!"
        )

    except Exception:
        messagebox.showerror(
            "Error",
            "Invalid Key or Cipher Text"
        )


def generate_hash():
    try:
        text = input_text.get(
            "1.0",
            tk.END
        ).strip()

        if not text:
            messagebox.showwarning(
                "Warning",
                "Enter text first!"
            )
            return

        sha_hash = hashlib.sha256(
            text.encode()
        ).hexdigest()

        output_text.delete("1.0", tk.END)
        output_text.insert(
            tk.END,
            sha_hash
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def clear_all():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    key_entry.delete(0, tk.END)

# =========================
# GUI
# =========================

root = tk.Tk()
root.title("🔐 Cryptography Suite")
root.geometry("900x700")
root.resizable(False, False)

# Colors
BG = "#1E1E2F"
FRAME = "#2B2D42"
BTN = "#3A86FF"
BTN_ACTIVE = "#2563EB"
TXT_BG = "#F8F9FA"
WHITE = "white"

root.configure(bg=BG)

# ------------------ Title ------------------

title = tk.Label(
    root,
    text="🔐 Cryptography Algorithms Implementation",
    font=("Segoe UI", 22, "bold"),
    bg=BG,
    fg="#00E5FF"
)
title.pack(pady=15)

# ------------------ Key Frame ------------------

frame_key = tk.Frame(
    root,
    bg=FRAME,
    bd=2,
    relief="ridge",
    padx=10,
    pady=10
)
frame_key.pack(pady=10)

tk.Label(
    frame_key,
    text="AES-128 Key",
    bg=FRAME,
    fg=WHITE,
    font=("Segoe UI", 11, "bold")
).grid(row=0, column=0, padx=5)

key_entry = tk.Entry(
    frame_key,
    width=45,
    font=("Consolas",11),
    bg=TXT_BG,
    relief="flat"
)
key_entry.grid(row=0,column=1,padx=10)

tk.Button(
    frame_key,
    text="Generate Key",
    command=generate_key,
    bg=BTN,
    fg="white",
    activebackground=BTN_ACTIVE,
    activeforeground="white",
    relief="flat",
    font=("Segoe UI",10,"bold"),
    cursor="hand2",
    padx=10
).grid(row=0,column=2)

# ------------------ Input ------------------

tk.Label(
    root,
    text="Input Text",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI",12,"bold")
).pack()

input_text = scrolledtext.ScrolledText(
    root,
    width=90,
    height=10,
    font=("Consolas",11),
    bg=TXT_BG,
    relief="flat"
)
input_text.pack(pady=8)

# ------------------ Buttons ------------------

button_frame = tk.Frame(root,bg=BG)
button_frame.pack(pady=15)

button_style = {
    "width":15,
    "height":2,
    "bg":BTN,
    "fg":"white",
    "font":("Segoe UI",10,"bold"),
    "relief":"flat",
    "activebackground":BTN_ACTIVE,
    "activeforeground":"white",
    "cursor":"hand2"
}

tk.Button(
    button_frame,
    text="🔒 AES Encrypt",
    command=aes_encrypt,
    **button_style
).grid(row=0,column=0,padx=8)

tk.Button(
    button_frame,
    text="🔓 AES Decrypt",
    command=aes_decrypt,
    **button_style
).grid(row=0,column=1,padx=8)

tk.Button(
    button_frame,
    text="🧮 SHA-256 Hash",
    command=generate_hash,
    **button_style
).grid(row=0,column=2,padx=8)

tk.Button(
    button_frame,
    text="🗑 Clear",
    command=clear_all,
    bg="#E63946",
    fg="white",
    font=("Segoe UI",10,"bold"),
    relief="flat",
    activebackground="#C1121F",
    activeforeground="white",
    cursor="hand2",
    width=15,
    height=2
).grid(row=0,column=3,padx=8)

# ------------------ Output ------------------

tk.Label(
    root,
    text="Output",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI",12,"bold")
).pack()

output_text = scrolledtext.ScrolledText(
    root,
    width=90,
    height=12,
    font=("Consolas",11),
    bg=TXT_BG,
    relief="flat"
)
output_text.pack(pady=8)

# ------------------ Footer ------------------

footer = tk.Label(
    root,
    text="AES Encryption  •  AES Decryption  •  SHA-256 Hashing",
    bg=BG,
    fg="#A8DADC",
    font=("Segoe UI",11)
)
footer.pack(pady=15)

root.mainloop()