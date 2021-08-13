from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


BG_COLOR = "#212529"
FG_COLOR = "#ced4da"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SEARCH FUNCTION ------------------------------- #


def search():
    """Search in the data file if the website name that was give exist
    if it does it returns the account details associated to the website
    else pops an error message"""
    website = website_entry.get().title()

    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data.keys():
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Oops", message="No account was found!")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    """Saves the website email and password that the user has input to a txt file"""

    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open(file="data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open(file="data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BG_COLOR)

canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=2, row=1)

# Labels
website_label = Label(text="Website:", bg=BG_COLOR, fg=FG_COLOR, font="Arial 12")
website_label.grid(column=1, row=2)
email_label = Label(text="Email/Username:", bg=BG_COLOR, fg=FG_COLOR, font="Arial 12")
email_label.grid(column=1, row=3)
password_label = Label(text="Password:", bg=BG_COLOR, fg=FG_COLOR, font="Arial 12")
password_label.grid(column=1, row=4)

# Entries
website_entry = Entry()
website_entry.grid(column=2, row=2, sticky="ew", ipady=3)
website_entry.focus()
email_entry = Entry()
email_entry.grid(column=2, row=3, columnspan=2, sticky="ew", ipady=3, pady=(5, 5))
email_entry.insert(0, "nhftk2005@gmail.com")
password_entry = Entry()
password_entry.grid(column=2, row=4, sticky="ew", ipady=3)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=3, row=4, padx=(10, 0))
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=2, row=5, columnspan=2, sticky="ew", pady=5)
search_button = Button(text="Search", command=search)
search_button.grid(column=3, row=2, sticky="ew", padx=(10, 0))


window.mainloop()
