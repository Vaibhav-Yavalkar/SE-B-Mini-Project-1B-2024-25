import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox 
from subprocess import call, Popen
import mysql.connector
from PIL import ImageTk, Image
import re
from bs4 import BeautifulSoup
import requests
from tkinter import messagebox
import webview
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import webbrowser
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.components()

    def components(self):
        self.Login_label = tk.Label(self, text='LOGIN', foreground='white',
                                    font=('Arial', 25, 'bold'),
                                    background='#242423', padx=30)
        self.Login_label.grid(row=0, column=1, pady=30)

        self.Username_Label = tk.Label(self, text='Email : ', foreground='white',
                                       font=('Times new Roman', 17),
                                       background='#242424', padx=5, pady=5)
        self.Username_Label.grid(row=1, column=0, padx=20, pady=50, sticky="ew")

        self.username_input = ctk.CTkEntry(self, placeholder_text='Enter Email')
        self.username_input.grid(row=1, column=1, pady=10, sticky="ew")

        self.Password_Label = tk.Label(self, text='Password :', foreground='white',
                                       font=('Times new Roman', 17),
                                       background='#242424', padx=5, pady=5)
        self.Password_Label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.password_input = ctk.CTkEntry(self, placeholder_text='Enter Password', show='*')
        self.password_input.grid(row=2, column=1, pady=10, sticky="ew")

        self.register_button = ctk.CTkButton(self, text='Register Here', command=self.controller.show_registration)
        self.register_button.grid(row=4, column=1, pady=10)

        self.login_button = ctk.CTkButton(self, text='Login', command=self.login)
        self.login_button.grid(row=3, column=1, pady=30)

    def login(self):
        username = self.username_input.get()
        password = self.password_input.get()
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='YOUR_PASSWORD',
            database='newsapp'
        )

        cursor = db.cursor()
        check_sql = "SELECT * from users where email_address = %s"

        cursor.execute(check_sql, (username,))
        soln = cursor.fetchone()

        if soln:
            print(soln)
            if password == soln[3]:
                messagebox.showinfo(message='Login Successful')
                self.controller.destroy()
                Dashboard(self.controller, soln[0], soln[2]).mainloop() 
            else:
                messagebox.showinfo(message='Incorrect password')
        else:
            messagebox.showinfo(message='Username not found')

        db.close()


class RegistrationPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_interests = []  # Store selected interests
        self.components()

    def connection(self, name, email_address, password, interests):
        try:
            self.db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='YOUR_PASSWORD',
                database='newsapp'
            )
            self.cursor = self.db.cursor()

            interest_str = ", ".join(interests)  # Convert list to string

            query = "INSERT INTO users(name, email_address, password, interest) VALUES (%s, %s, %s, %s)"
            val = (name, email_address, password, interest_str)

            self.cursor.execute(query, val)
            self.db.commit()
            messagebox.showinfo(message="Registration Successful")

        except mysql.connector.Error as err:
            messagebox.showerror(message=f"Database Error: {err}")

        finally:
            self.cursor.close()
            self.db.close()

    def components(self):
        self.Login_label = tk.Label(self, text='Registration', foreground='white',
                                    font=('Arial', 25, 'bold'),
                                    background='#242423', padx=30)
        self.Login_label.grid(row=0, column=1, pady=30)

        self.NameLabel = tk.Label(self, text='Name : ', foreground='white',
                                  font=('Times New Roman', 17),
                                  background='#242424', padx=5, pady=5)
        self.NameLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.name_input = ctk.CTkEntry(self, placeholder_text='Enter name')
        self.name_input.grid(row=1, column=1, pady=10, sticky="ew")

        self.email_label = tk.Label(self, text='Email address : ', foreground='white',
                                    font=('Times New Roman', 17),
                                    background='#242424', padx=5, pady=5)
        self.email_label.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.email_input = ctk.CTkEntry(self, placeholder_text='Enter email')
        self.email_input.grid(row=2, column=1, pady=10, sticky="ew")

        self.Password_Label = tk.Label(self, text='Password :', foreground='white',
                                       font=('Times New Roman', 17),
                                       background='#242424', padx=5, pady=5)
        self.Password_Label.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.password_input = ctk.CTkEntry(self, placeholder_text='Enter Password', show='*')
        self.password_input.grid(row=3, column=1, pady=10, sticky="ew")

        self.Interest_Label = tk.Label(self, text='Interest :', foreground='white',
                                       font=('Times New Roman', 17),
                                       background='#242424', padx=5, pady=5)
        self.Interest_Label.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        self.checkboxes()

    def checkboxes(self):
        self.checkboxes_list = {
            "Sports": tk.IntVar(),
            "Finance": tk.IntVar(),
            "Entertainment": tk.IntVar(),
            "World": tk.IntVar(),
            "Politics": tk.IntVar(),
            "Science/Tech": tk.IntVar(),
        }

        self.checkbox_widgets = []
        row_num = 4
        col_num = 1

        for index, (label, var) in enumerate(self.checkboxes_list.items()):
            checkbox = ctk.CTkCheckBox(self, text=label, variable=var,
                                    fg_color='#47574F', font=('Helvetica', 18, 'bold'))
            checkbox.grid(row=row_num, column=col_num, pady=5, padx=5, sticky="w")
            self.checkbox_widgets.append(checkbox)

            col_num += 1
            if col_num > 2:
                col_num = 1
                row_num += 1  # Move to the next row

        self.register_button = ctk.CTkButton(self, text='Register Here', command=self.button_event)
        self.register_button.grid(row=row_num + 1, column=1, pady=20)  # Pushed below checkboxes

    def get_selected_interests(self):
        return [label for label, var in self.checkboxes_list.items() if var.get() == 1]

    def already_exist(self, email_address):
        try:
            self.db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='YOUR_PASSWORD',
                database='newsapp'
            )
            self.cursor = self.db.cursor()

            query = "SELECT * FROM users WHERE email_address = %s"
            self.cursor.execute(query, (email_address,))
            return self.cursor.fetchone() is not None

        except mysql.connector.Error as err:
            messagebox.showerror(message=f"Database Error: {err}")
            return False

        finally:
            self.cursor.close()
            self.db.close()

    def button_event(self):
        name = self.name_input.get().strip()
        email = self.email_input.get().strip()
        password = self.password_input.get().strip()
        interests = self.get_selected_interests()

        if not name.isalpha():
            messagebox.showerror(message='Only alphabets allowed in the name field.')
        elif len(password) < 6:
            messagebox.showerror(message='Password must be at least 6 characters long.')
        elif not self.validate_email(email):
            messagebox.showerror(message='Invalid email format.')
        elif self.already_exist(email):
            messagebox.showerror(message='This email is already registered.')
        elif not interests:
            messagebox.showerror(message='Please select at least one interest.')
        else:
            self.connection(name, email, password, interests)

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("750x550")
        self.title("BuzzFeed")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for Page in (LoginPage, RegistrationPage):
            page_name = Page.__name__
            page = Page(self.container, self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_login()

    def show_login(self):
        self.show_frame("LoginPage")

    def show_registration(self):
        self.show_frame("RegistrationPage")

    def show_frame(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()



class Dashboard(ctk.CTk):
    def __init__(self, parent, login_number, email_address):
        super().__init__()
        self.parent = parent
        self.title("News App Dashboard")
        self.geometry(f"{1000}x{600}")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.initframes()
        self.initcomponents()
        self.headline_list = []
        self.href_list = []
        self.login_number = login_number  
        self.email_id = email_address
        print(self.login_number, self.email_id)
    def initframes(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", columnspan = 2)
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight = 1)
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=2, sticky="nsew", rowspan = 5, columnspan = 5)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
    def initcomponents(self):
        self.dashboardLabel = ctk.CTkLabel(self.sidebar_frame, text="Dashboard", font = ('Arial', 20, 'bold'))
        self.dashboardLabel.grid(row = 0, column = 0, pady = 20)

        self.search_button = tk.Button(self.sidebar_frame, text="Search News", height=3,  font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white', command=self.search_news)
        self.search_button.grid(row=2, column=0, sticky= 'nsew', pady= 15)

        self.category_button = tk.Button(self.sidebar_frame, text="News by Category", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',  command=self.news_by_category)
        self.category_button.grid(row=3, column=0, sticky= 'new', pady = 15)

        self.infographics_button = tk.Button(self.sidebar_frame, text="Infographics", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white', command=self.infographics)
        self.infographics_button.grid(row=4, column=0, sticky= 'new', pady = 15)

        self.myprofile_button = tk.Button(self.sidebar_frame, text="My Profile", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white', command=self.profile)
        self.myprofile_button.grid(row=5, column=0, sticky= 'new', pady = 15)

        self.Logout_button = tk.Button(self.sidebar_frame, text="Log out", height=1, font = ('Arial', 12, 'bold'), background='#14497E', foreground= 'white', command = self.loginPage)
        self.Logout_button.grid(row=7, column=0, sticky= 'ws', pady = 0)

        self.dailyNewsLabel = ctk.CTkLabel(self.scrollable_frame, text="Daily News", font=('Arial', 25, 'bold'))
        self.dailyNewsLabel.grid(row=0, column=0, sticky='nsew')

        self.bookmark_button = ctk.CTkButton(self.scrollable_frame, text = 'bookmark', command= self.bookmark_action)
        self.bookmark_button.grid(row = 1, column = 3, sticky = 'w')
        

        self.fetch_and_display_headlines()


    def fetch_and_display_headlines(self):
        url = "https://www.bing.com/news"
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        headlines = soup.find_all('a', class_='title')
        titles = soup.find_all('div', class_='publogo')
        x = 2
        for index, (headline, title) in enumerate(zip(headlines, titles), start=1):
            if headline.text.strip() and title.text.strip() and title.text != 'Ad':
                href = headline.get('href')
                a = headline.text.strip() + ' by ' + ' ' +title.text.strip()
                #title_label = ctk.CTkLabel(self.scrollable_frame, text = title.text.strip(), bg_color= 'green')
                #title_label.grid(row = x + 1, column = 0)
                headline_button = ctk.CTkButton(self.scrollable_frame, text=a, width= 30,
                                                font=ctk.CTkFont(size=20, weight="bold"),
                                                command=lambda idx=index, href=href: self.show_headline(href))
                headline_button._text_label.configure(wraplength=499)
                headline_button.grid(row=index + 3, column= 0 ,  sticky="nsew", columnspan = 4, pady = (20, 0))

                self.bookmark_radio = ctk.CTkRadioButton(self.scrollable_frame, text = '', bg_color='#0168AA', width = 5 )
                #self.bookmark_radio.grid(row = index + 3, column = 3, stick = 'ew')
                self.scrollable_frame.grid_rowconfigure(index, weight= 0)

                #self.checkbox = ctk.CTkCheckBox(self.scrollable_frame, text = '', width = 1)
                #self.checkbox.grid(row = index + 3, column = 0, sticky = 'e')

    def bookmark_action(self) : 
        self.headline_dict = {}
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=2, sticky="nsew", rowspan = 5, columnspan = 5)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        url = "https://www.bing.com/news"
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        headlines = soup.find_all('a', class_='title')
        titles = soup.find_all('div', class_='publogo')
        x = 2
        for index, (headline, title) in enumerate(zip(headlines, titles), start=1):
            if headline.text.strip() and title.text.strip() and title.text != 'Ad':
                href = headline.get('href')
                a = headline.text.strip() + ' by ' + ' ' +title.text.strip()
                #title_label = ctk.CTkLabel(self.scrollable_frame, text = title.text.strip(), bg_color= 'green')
                #title_label.grid(row = x + 1, column = 0)
                headline_button = ctk.CTkButton(self.scrollable_frame, text=a, width= 30,
                                                font=ctk.CTkFont(size=20, weight="bold"),
                                                command=lambda idx=index, href=href: self.show_headline(href))
                headline_button._text_label.configure(wraplength=499)
                headline_button.grid(row=index + 3, column= 0 ,  sticky="nsew", columnspan = 4, pady = (20, 0))

                #self.bookmark_radio = ctk.CTkRadioButton(self.scrollable_frame, text = '', bg_color='#0168AA', width = 5 )
                #self.bookmark_radio.grid(row = index + 3, column = 3, stick = 'ew')
                self.scrollable_frame.grid_rowconfigure(index, weight= 1)

                self.check_var = ctk.StringVar(value="off")
                self.checkbox = ctk.CTkCheckBox(self.scrollable_frame, text = '', width = 1,  command = lambda sv = self.check_var, a = a, href = href: self.checkbox_event(sv, a, href), 
                                                variable=self.check_var, onvalue="on", offvalue="off")
                self.checkbox.grid(row = index + 3, column = 1, sticky = 'e')
                self.headline_dict[a] = self.check_var

        self.confirm_bookmark = ctk.CTkButton(self.scrollable_frame, text = 'bookmark confirm ', command= self.bookmark_confirm)
        self.confirm_bookmark.grid(row = index, column = 1, sticky = 'e', pady = 10)
        

    def checkbox_event(self, var, headline, href):
        #print("checkbox for ", var.get(), headline)
        
        if var.get() == "on":
            self.headline_list.append(headline)
            self.href_list.append(href)
        if var.get() == 'off':
            if headline in self.headline_list and href in self.href_list:
                self.headline_list.remove(headline)
                self.href_list.remove(href)


    def bookmark_confirm(self):
        
        # print(self.headline_list)
        # print(self.href_list)
        # for i in range(len(self.headline_list)):
        #     print(self.headline_list[i])
        #     print(self.href_list[i])
        #     print('\n')

        self.insert_in_database()
        messagebox.showinfo(message="Bookmarks confirmed")
        self.initframes()
        self.initcomponents()
        self.headline_list = []
        self.href_list = []
        self.bookmark_button = ctk.CTkButton(self.scrollable_frame, text = 'bookmark', command= self.bookmark_action)
        self.bookmark_button.grid(row = 1, column = 3, sticky = 'w')
        self.fetch_and_display_headlines()

    def insert_in_database(self):
        self.db = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'YOUR_PASSWORD',
            database = 'newsapp'
        )
        # print(self.db)
        self.cursor = self.db.cursor()
        query = "INSERT INTO bookmarks (user_id, headline, href) VALUES (%s, %s, %s)"
        for headline, href in zip(self.headline_list, self.href_list):
            self.cursor.execute(query, (self.login_number, headline, href))
        self.db.commit()

    def search_news(self):
        self.destroy()
        search_app = SearchEmail(self.email_id, self.login_number)
        search_app.mainloop()

    def news_by_category(self):
        self.destroy()
        news_app = NewsCategory(self.email_id, self.login_number)
        news_app.mainloop()

    def infographics(self):
        self.destroy()
        news_app = NewsAppInfographics(self.email_id, self.login_number)
        news_app.mainloop()

    def show_headline(self, link):
        webview.create_window('News Headline', link)
        webview.start()

    def profile(self):
        self.destroy()
        print(self.login_number)
        news_app = NewsAppDashboardProfile(self.login_number)
        news_app.mainloop()


    def loginPage(self):

        self.destroy()
        App().mainloop()


class SearchEmail(ctk.CTk):
    def __init__(self, email_address, login_number):
        super().__init__()
        self.title("Search and Get news")
        self.geometry(f"{1000}x{600}")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight =1)
        self.grid_columnconfigure((2, 3), weight = 1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.initframes()
        self.initcomponents()
        self.headlines_list = []
        self.links_list = []
        self.email_address = email_address
        self.login_number = login_number
    def initframes(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", columnspan = 2)
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight = 1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)

        self.scrollable_frame.grid(row=0, column=2, sticky="nsew", rowspan = 5, columnspan = 5)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

    def initcomponents(self):
        self.dashboardLabel = ctk.CTkLabel(self.sidebar_frame, text="Search News", font = ('Arial', 20, 'bold'))
        self.dashboardLabel.grid(row = 0, column = 0, pady = 20)
        self.DashboardButton = tk.Button(self.sidebar_frame, text="Dashboard", height=3,  font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white', command=self.dashboard)
        self.DashboardButton.grid(row=2, column=0, sticky= 'nsew', pady= 15)

        self.category_button = tk.Button(self.sidebar_frame, text="News by Category", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white', command=self.news_by_category)
        self.category_button.grid(row=3, column=0, sticky= 'new', pady = 15)

        self.infographics_button = tk.Button(self.sidebar_frame, text="Infographics", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white', command=self.infographics)
        self.infographics_button.grid(row=4, column=0, sticky= 'new', pady = 15)

        self.myprofile_button = tk.Button(self.sidebar_frame, text="My Profile", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white', command=self.profile)
        self.myprofile_button.grid(row=5, column=0, sticky= 'new', pady = 15)

        self.Logout_button = tk.Button(self.sidebar_frame, text="Log out", height=1, font = ('Arial', 12, 'bold'), background='#14497E', foreground= 'white', command = self.loginPage)
        self.Logout_button.grid(row=7, column=0, sticky= 'ws', pady = 0)

        self.dailyNewsLabel = ctk.CTkLabel(self.scrollable_frame, text="Enter keyword to search for that news", font=('Arial', 20, 'bold'))
        self.dailyNewsLabel.grid(row=0, column=0, sticky='nsew')

        self.SearchEntry = ctk.CTkEntry(self.scrollable_frame, placeholder_text= 'Enter keyword here to serach')
        self.SearchEntry.grid(row = 1, column = 0, sticky = 'nsew', pady = 20)

        self.SearchButton = ctk.CTkButton(self.scrollable_frame, text = 'search', font=ctk.CTkFont(weight="bold"),
                                           command= lambda : self.getnews())
        self.SearchButton.grid(row = 1, column = 1, sticky = 'ew', pady = 20, padx = 5)

        self.GetEmailButton = ctk.CTkButton(self.scrollable_frame, text = 'Get this News on Email', font=ctk.CTkFont(weight="bold"), command = self.sendemail) 
    

    def getnews(self):

        query = self.SearchEntry.get()
        if query == '':
            messagebox.showinfo('Inavlid Query',message='Empty Query, Please enter something')

        if query.isdigit():
            messagebox.showinfo('Invalid Query', message= 'Seacrh Query cannot consist of numbers')

        else :
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}
            url = "https://www.bing.com/news/search?q={}"
            html = requests.get(url.format(query), headers=headers)
            soup = BeautifulSoup(html.text, "lxml")
            x = 2
            for result in soup.select('.card-with-cluster'):
                headline = result.select_one('.title')
                if headline.text.strip():
                    href = headline.get('href')
                    self.headlineButton = ctk.CTkButton(self.scrollable_frame, text = headline.text.strip(), width=30,
                                                        font=ctk.CTkFont(size=20, weight="bold"), 
                                                        command= lambda href = href : self.GotoNews(href))
                    self.headlineButton._text_label.configure(wraplength=499)
                    self.headlineButton.grid(row = x, column = 0, pady = 5, sticky = 'nsew', columnspan = 5 )
                    x += 1
                    self.headlines_list.append(headline.text.strip())
                    self.links_list.append(href)
            self.GetEmailButton.grid(row = x + 1 , column = 0, columnspan = 5, pady = 10)
    
    def sendemail(self):
        my_email = "buzzfeedproject123@gmail.com"
        password = "elkx abhg pezs ofgn"
        to_email = self.email_address
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=my_email, password=password)
        
        msg = MIMEMultipart()
        msg['From'] = my_email
        msg['To'] = to_email
        msg['Subject'] = "Your Daily News Update"

        # HTML email body with purple color scheme
        html_body = """
        <html>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <div style="background-color: #6B48FF; padding: 20px; color: white;">
                        <h1 style="margin: 0; font-size: 24px;">Your Daily News Update</h1>
                    </div>
                    
                    <!-- Content -->
                    <div style="padding: 20px;">
                        <p style="color: #333; font-size: 16px; margin: 0 0 20px 0;">Here are the latest news headlines:</p>
        """

        # Add headlines and links
        for headline, link in zip(self.headlines_list, self.links_list):
            html_body += f"""
                        <div style="margin-bottom: 20px;">
                            <a href="{link}" style="text-decoration: none; color: #6B48FF; font-size: 18px; font-weight: bold; display: block; margin-bottom: 5px;">
                                {headline}
                            </a>
                            <a href="{link}" style="text-decoration: none; color: #9333FF; font-size: 14px;">
                                Read More →
                            </a>
                        </div>
            """

        # Footer
        html_body += """
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f0edff; padding: 15px; text-align: center; color: #666; font-size: 12px;">
                    </div>
                </div>
            </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))
        connection.sendmail(from_addr=my_email, to_addrs=to_email, msg=msg.as_string())
        messagebox.showinfo("Success", "Email sent successfully!")
        connection.quit()

    def dashboard(self):
        email = self.email_address
        login_number = self.login_number
        print("Search Email Page: ", login_number, email)
        self.destroy()
        news_app = Dashboard(None, login_number, email)
        news_app.mainloop()

    def news_by_category(self):
        self.destroy()
        news_app = NewsCategory(self.email_address, self.login_number)
        news_app.mainloop()

    def infographics(self):
        self.destroy()
        news_app = NewsAppInfographics(self.email_id, self.login_number)
        news_app.mainloop()
    
    def profile(self):
        self.destroy()
        print(self.login_number)
        news_app = NewsAppDashboardProfile(self.login_number)

        news_app.mainloop()

    def GotoNews(self, link):
        webview.create_window('News Headline', link)
        webview.start()

    def loginPage(self):
        self.destroy()
        App().mainloop()



class NewsCategory(ctk.CTk):
    def __init__(self, email_id, login_number):
        super().__init__()
        self.geometry(f"{1000}x{600}")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.initframes()
        self.initcomponents()
        self.initscrollable()
        self.login_number = login_number
        self.email_id = email_id

    def initframes(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", columnspan = 2)
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight = 1)
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=2, sticky="nsew", rowspan = 5, columnspan = 5)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
    def initscrollable(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=2, sticky="nsew", rowspan = 5, columnspan = 5)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.NewsCategory = ctk.CTkLabel(self.scrollable_frame, text = "News category", font=('Arial', 25, 'bold'))
        self.NewsCategory.grid(row = 0, column = 0, sticky = 'nsew', pady = 15)
        self.checkboxes()

    def initcomponents(self):

        self.NewsCategoryLabel = ctk.CTkLabel(self.sidebar_frame, text="News Category", font = ('Arial', 20, 'bold'))
        self.NewsCategoryLabel.grid(row = 0, column = 0, pady = 20)

        self.Dashboard_button = tk.Button(self.sidebar_frame, text="Dashboard", height=3,  font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',
                                          command=self.dashboard)
        self.Dashboard_button.grid(row=2, column=0, sticky= 'nsew', pady= 15)

        self.SearchNews_button = tk.Button(self.sidebar_frame, text="Search News", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',
                                           command=self.search_news)
        self.SearchNews_button.grid(row=3, column=0, sticky= 'new', pady = 15)

        self.infographics_button = tk.Button(self.sidebar_frame, text="Infographics", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',
                                             command=self.infographics)
        self.infographics_button.grid(row=4, column=0, sticky= 'new', pady = 15)

        self.myprofile_button = tk.Button(self.sidebar_frame, text="My Profile", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',
                                          command=self.profile)
        self.myprofile_button.grid(row=5, column=0, sticky= 'new', pady = 15)

        self.Logout_button = tk.Button(self.sidebar_frame, text="Log out", height=1, font = ('Arial', 12, 'bold'), background='#14497E', foreground= 'white',
                                       command=self.loginPage)
        self.Logout_button.grid(row=7, column=0, sticky= 'ws', pady = 0)

        self.NewsCategory = ctk.CTkLabel(self.scrollable_frame, text = "News category", font=('Arial', 25, 'bold'))
        self.NewsCategory.grid(row = 0, column = 0, sticky = 'nsew', pady = 15)



        self.checkboxes()
      


    def state_of_checkoox(self, index):
        checkboxes_list = [self.SportsCheckbox, self.FinanceCheckbox, self.EntertainmentCheckbox, self.WorldNewsbox, 
                      self.Politicsbox, self.SciTechbox]
        checkbox_text = ["Sports", "Finance", "Entertainment", "World", "Politics", "Sci/Tech"]
        current_checkbox = checkboxes_list[index]
        current_selection = checkbox_text[index]
        if current_checkbox.get() == 1:
            print(current_selection)
            self.CheckBoxLabel = ctk.CTkLabel(self.scrollable_frame, text=(' '*5) + current_selection + (' '*5), font = ( 'Helvetica', 20, 'bold'),
                                              width = 30)
            self.CheckBoxLabel.grid(row = 3, column = 0 , pady = 4)
            for checkbox in checkboxes_list:
                if checkbox != current_checkbox:
                    checkbox.configure(state='disabled')
            self.getnewsbycategory(index)
        else :
            
            self.CheckBoxLabel.destroy()
            self.initscrollable()
            for checkbox in checkboxes_list:
                checkbox.configure(state='enabled')
                self.checkboxes()
    
    def checkboxes(self):
        self.SportsCheckbox = ctk.CTkCheckBox(self.scrollable_frame, text = "Sports", 
                                              fg_color= '#47574F', font = ( 'Helvetica', 18, 'bold'),
                                              onvalue=1, offvalue= 0,
                                              command=lambda :self.state_of_checkoox(0))
        self.SportsCheckbox.grid(row = 1, column = 0, pady = 5, padx = 5)

        self.FinanceCheckbox = ctk.CTkCheckBox(self.scrollable_frame, text = "Finance", 
                                              fg_color= '#47574F', font = ( 'Helvetica', 18, 'bold'),
                                              onvalue=1, offvalue= 0,
                                              command=lambda: self.state_of_checkoox(1))
        self.FinanceCheckbox.grid(row = 1, column = 1, pady = 5, padx = 5)


        self.EntertainmentCheckbox = ctk.CTkCheckBox(self.scrollable_frame, text = "Entertainment", 
                                              fg_color= '#47574F', font = ( 'Helvetica', 18, 'bold'),
                                              onvalue=1, offvalue= 0,
                                              command=lambda : self.state_of_checkoox(2))
        self.EntertainmentCheckbox.grid(row = 1, column = 2, pady = 5, padx = 5)


        self.WorldNewsbox = ctk.CTkCheckBox(self.scrollable_frame, text = "World", 
                                              fg_color= '#47574F', font = ( 'Helvetica', 18, 'bold'),
                                              onvalue= 1, offvalue=0,
                                              command=lambda :self.state_of_checkoox(3))
        self.WorldNewsbox.grid(row = 2, column = 0, pady = 15, padx = 5)

        self.Politicsbox = ctk.CTkCheckBox(self.scrollable_frame, text = "Politics", 
                                              fg_color= '#47574F', font = ( 'Helvetica', 18, 'bold'),
                                              onvalue=1, offvalue= 0,
                                              command=lambda :self.state_of_checkoox(4))
        self.Politicsbox.grid(row = 2, column = 1, pady = 15, padx = 5)


        self.SciTechbox = ctk.CTkCheckBox(self.scrollable_frame, text = "Science/Tech", 
                                              fg_color= '#47574F', font = ( 'Helvetica', 18, 'bold'),
                                              onvalue=1, offvalue= 0,
                                              command=lambda :self.state_of_checkoox(5))
        self.SciTechbox.grid(row = 2, column = 2, pady = 15, padx = 5)
    



    def getnewsbycategory(self, index):
        checkbox_text = ["Sports", "Finance", "Entertainment", "World", "Politics", "Sci/Tech"]
        
        format_list = ['Sports', 'Business', 'Entertainment', 'World', 'Politics', 'Sci%2fTech']
        url = f"https://www.bing.com/news/search?q={format_list[index]}"
        print(url)
        # testurl = "https://www.bing.com/news/search?q={Sports}"

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}

        request = requests.get(url)
        
        soup = BeautifulSoup(request.text, 'lxml')

        x = 4
        headlines = soup.find_all('div', class_ = 'na_t news_title ns_big')
        links = soup.find_all('a', class_='news_fbcard wimg')
        results = soup.select('a', class_= 'news_fbcard wimg')



        for headline, link in zip(headlines, links):
            href = link.get('href')
            self.headlineButton = ctk.CTkButton(self.scrollable_frame, text = headline.text.strip(), width=30,
                                            font=ctk.CTkFont(size=20, weight="bold"), 
                                             command= lambda href = href : self.show_headline(href))
            self.headlineButton._text_label.configure(wraplength=499)
            self.headlineButton.grid(row = x, column = 0, pady = 5, sticky = 'nsew', columnspan = 5 )
            self.bookmark_radio = ctk.CTkRadioButton(self.scrollable_frame, text = '', bg_color='#0168AA', width = 5, fg_color= 'white' )
            self.bookmark_radio.grid(row =x, column = 3, stick = 'ew', )
            x += 1


    def GotoNews(self, link):
         webbrowser.open(link)

    def dashboard(self):
        self.destroy()
        print("News Category : ", self.login_number, self.email_id)
        news_app = Dashboard(None, self.email_id, self.login_number)

    def search_news(self):
        self.destroy()
        search_app = SearchEmail(self.email_id, self.login_number)
        search_app.mainloop()

    def infographics(self):
        self.destroy()
        news_app = NewsAppInfographics(self.email_id, self.login_number)
        news_app.mainloop()

    def show_headline(self, link):

        webview.create_window('News Headline', link)
        webview.start()

    def profile(self):
        self.destroy()
        print(self.login_number)
        news_app = NewsAppDashboardProfile(self.login_number)
        news_app.mainloop()

    def loginPage(self):
        self.destroy()
        App().mainloop()

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import requests
from bs4 import BeautifulSoup
import webview

class NewsAppDashboardProfile(ctk.CTk):
    def __init__(self, login_number):
        super().__init__()
        self.title("News App Dashboard")
        self.geometry(f"{1000}x{600}")
        self.resizable(False, False)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        
        self.initframes()
        self.initcomponents()
        
        self.login_number = login_number
        print("Profile : ", self.login_number)
        self.profilecomponents(self.login_number)
        
        self.email_address = None
        self.headline_list = []
        self.href_list = []

    def initframes(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", columnspan=2)
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=2, sticky="nsew", rowspan=10, columnspan=10)
        self.scrollable_frame.grid_columnconfigure(1, weight=0)

    def initcomponents(self):
        self.myprofile_label = ctk.CTkLabel(self.sidebar_frame, text="My Profile", font=('Arial', 20, 'bold'))
        self.myprofile_label.grid(row=0, column=0, pady=20)

        self.dashboard_button = tk.Button(self.sidebar_frame, text="Dashboard", height=3, font=('Arial', 14, 'bold'), 
                                          background='#14476E', foreground='white', command=self.dashboard)
        self.dashboard_button.grid(row=2, column=0, sticky='nsew', pady=15)

        self.search_button = tk.Button(self.sidebar_frame, text="Search News", height=3, font=('Arial', 14, 'bold'), 
                                       background='#14476E', foreground='white', command=self.search_news)
        self.search_button.grid(row=3, column=0, sticky='nsew', pady=15)

        self.category_button = tk.Button(self.sidebar_frame, text="News by Category", height=3, font=('Arial', 14, 'bold'), 
                                         background='#14476E', foreground='white', command=self.news_by_category)
        self.category_button.grid(row=4, column=0, sticky='new', pady=15)

        self.infographics_button = tk.Button(self.sidebar_frame, text="Infographics", height=3, font=('Arial', 14, 'bold'), 
                                             background='#14476E', foreground='white', command=self.infographics)
        self.infographics_button.grid(row=5, column=0, sticky='new', pady=15)

        self.logout_button = tk.Button(self.sidebar_frame, text="Log out", height=1, font=('Arial', 12, 'bold'), 
                                       background='#14497E', foreground='white', command=self.loginPage)
        self.logout_button.grid(row=7, column=0, sticky='ws', pady=0)

        self.my_profile_label = ctk.CTkLabel(self.scrollable_frame, text="My Profile", font=('Arial', 25, 'bold'))
        self.my_profile_label.grid(row=0, column=0, sticky='nsew')

    def profilecomponents(self, login_number):
        self.scrollable_frame.grid_columnconfigure(0, weight=0)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

        profile_name_label = ctk.CTkLabel(self.scrollable_frame, text=" Name : ", font=('serif', 19, 'bold'))
        profile_name_label.grid(row=1, column=1, sticky='nw', pady=15)
        
        self.fetch_name(login_number)
        self.fetch_bookmarks(login_number)

        # Display bookmarks directly below the label
        self.display_bookmarks()

    def fetch_name(self, login_number):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='YOUR_PASSWORD',
            database='newsapp'
        )
        self.cursor = self.db.cursor()
        query = "SELECT name, email_address, interest FROM users WHERE id = %s"
        self.cursor.execute(query, (login_number,))
        
        for row in self.cursor.fetchall():
            name, email, interest = row
            self.email_address = email
            profile_name_label = ctk.CTkLabel(self.scrollable_frame, text=" Name : " + name, font=('serif', 19, 'bold'))
            profile_name_label.grid(row=1, column=1, sticky='nw', pady=15)
            profile_email_label = ctk.CTkLabel(self.scrollable_frame, text=" Email : " + email, font=('serif', 19, 'bold'))
            profile_email_label.grid(row=2, column=1, sticky='nw', pady=15)
            profile_interest_label = ctk.CTkLabel(self.scrollable_frame, text=" Interest : " + interest, font=('serif', 19, 'bold'))
            profile_interest_label.grid(row=3, column=1, sticky='nw', pady=15)
            profile_bookmark_label = ctk.CTkLabel(self.scrollable_frame, text=" Bookmarks : " ,font=('serif', 19, 'bold'))
            profile_bookmark_label.grid(row=4, column=1, sticky='nw', pady=15)
        
        self.cursor.close()
        self.db.close()

    def fetch_bookmarks(self, login_number):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='YOUR_PASSWORD',
            database='newsapp'
        )
        self.cursor = self.db.cursor()
        query = "SELECT headline, href FROM bookmarks WHERE user_id = %s"
        self.cursor.execute(query, (login_number,))

        self.headline_list = []
        self.href_list = []

        for headline, href in self.cursor:
            self.headline_list.append(headline)
            self.href_list.append(href)

        self.cursor.close()
        self.db.close()

    def display_bookmarks(self):
        if len(self.headline_list) > 0:
            for index, (headline, href) in enumerate(zip(self.headline_list, self.href_list), start=1):
                headline_button = ctk.CTkButton(self.scrollable_frame, text=headline, width=30,
                                                font=ctk.CTkFont(size=20, weight="bold"),
                                                command=lambda href=href: self.show_headline(href))
                headline_button._text_label.configure(wraplength=499)
                headline_button.grid(row=index + 4, column=0, sticky="nsew", columnspan=5, pady=(20, 0))

    def show_headline(self, link):
        webview.create_window('News Headline', link)
        webview.start()

    def dashboard(self):
        self.fetch_name(self.login_number)
        email = self.email_address
        self.destroy()
        print(email)
        news_app = Dashboard(None, self.login_number, email)
        news_app.mainloop()

    def search_news(self):
        self.fetch_name(self.login_number)
        email = self.email_address
        self.destroy()
        search_app = SearchEmail(email, self.login_number)
        search_app.mainloop()

    def news_by_category(self):
        self.fetch_name(self.login_number)
        email = self.email_address
        self.destroy()
        news_app = NewsCategory(email, self.login_number)
        news_app.mainloop()

    def infographics(self):
        self.fetch_name(self.login_number)
        email = self.email_address
        self.destroy()
        news_app = NewsAppInfographics(email, self.login_number)
        news_app.mainloop()

    def loginPage(self):
        self.destroy()
        App().mainloop()

    def GotoNews(self, link):
        webview.create_window('News Headline', link)
        webview.start()

class NewsAppInfographics(ctk.CTk):
    def __init__(self, email_id, login_number):
        super().__init__()

        self.title("News App Dashboard")
        self.geometry(f"{1000}x{600}")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.initframes()
        self.initcomponents()
        self.login_number = login_number
        self.email_address = email_id


    def initframes(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew", columnspan = 2)
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight = 1)
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=2, sticky="nsew", rowspan = 5, columnspan = 5)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

    def initcomponents(self):
        self.infographics_label = ctk.CTkLabel(self.sidebar_frame, text="Infographics", font = ('Arial', 20, 'bold'))
        self.infographics_label.grid(row = 0, column = 0, pady = 20)

        self.dashboard_button = tk.Button(self.sidebar_frame, text="Dashboard", height=3,  font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',
                                          command= self.dashboard)
        self.dashboard_button.grid(row=2, column=0, sticky= 'nsew', pady= 15)

        self.search_news_button = tk.Button(self.sidebar_frame, text="Search News", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',
                                            command= self.search_news)
        self.search_news_button.grid(row=3, column=0, sticky= 'new', pady = 15)

        self.category_button = tk.Button(self.sidebar_frame, text="News By Category", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',
                                         command=self.news_by_category)
        self.category_button.grid(row=4, column=0, sticky= 'new', pady = 15)

        self.myprofile_button = tk.Button(self.sidebar_frame, text="My Profile", height=3, font = ('Arial', 14, 'bold'), background='#14476E', foreground= 'white',
                                          command=self.profile)
        self.myprofile_button.grid(row=5, column=0, sticky= 'new', pady = 15)

        self.Logout_button = tk.Button(self.sidebar_frame, text="Log out", height=1, font = ('Arial', 12, 'bold'), background='#14497E', foreground= 'white')
        self.Logout_button.grid(row=7, column=0, sticky= 'ws', pady = 0)

        self.topics_label = ctk.CTkLabel(self.scrollable_frame, text="Topics", font=('Arial', 25, 'bold'))
        self.topics_label.grid(row=0, column=0, sticky='nsew', padx = 10)


        self.economics_button = tk.Button(self.scrollable_frame, text = 'Economics', font = ('Helavetica', 22), background='white', command=self.show_economics)
        self.economics_button.grid(row = 1, column= 0,  pady = 15, columnspan= 5, rowspan= 5, sticky='nsew')
        # self.ent_button = tk.Button(self.scrollable_frame, text = 'Entertainment', font = ('Helavetica', 22), background='white', command=self.show_entartiment)
        # self.ent_button.grid(row = 11, column= 0,  pady = 15, columnspan= 5, rowspan= 10, sticky='nsew')
        self.health_button = tk.Button(self.scrollable_frame, text = 'Health & Nutrition', font = ('Helavetica', 22), background='white', command=self.show_health)
        self.health_button.grid(row = 11, column= 0,  pady = 15, columnspan= 5, rowspan= 10, sticky='nsew')
        self.conflict_button = tk.Button(self.scrollable_frame, text = 'Fraglity, Conflict & Violence', font = ('Helavetica', 22), background='white', command=self.show_fragility)
        self.conflict_button.grid(row = 21, column= 0,  pady = 15, columnspan= 5, rowspan= 10, sticky='nsew')
        self.env_button = tk.Button(self.scrollable_frame, text = 'Environment & Resources', font = ('Helavetica', 22), background='white', command=self.show_environment)
        self.env_button.grid(row = 31, column= 0,  pady = 15, columnspan= 5, rowspan= 10, sticky='nsew')
        

    def show_economics(self):
        self.gdp_button = ctk.CTkButton(self.scrollable_frame, text = 'GDP per Capita of India (1960-2022) ', font = ('Helavetica', 15), command=self.display_graph_gdp)
        self.gdp_button.grid(row = 52, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
        self.inflation_button = ctk.CTkButton(self.scrollable_frame, text = 'Inflation, consumer prices (annual % 1960- 2022)', font = ('Helavetica', 15), command=self.display_graph_inflation)
        self.inflation_button.grid(row = 54, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
        self.une_button = ctk.CTkButton(self.scrollable_frame, text = 'Unemployement, female (% of female labor force)', font = ('Helavetica', 15), command=self.display_graph_une)
        self.une_button.grid(row = 56, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)


    def show_health(self):
        self.birth_rate_button = ctk.CTkButton(self.scrollable_frame, text = 'Birth rate, crude (per 1,000 people) ', font = ('Helavetica', 15), command=self.display_birth_rate)
        self.birth_rate_button.grid(row = 52, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
        self.hiv_button = ctk.CTkButton(self.scrollable_frame, text = 'Prevalence of HIV, total (% of population ages 15-49)', font = ('Helavetica', 15), command=self.display_hiv)
        self.hiv_button.grid(row = 54, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
        self.sanitation_button = ctk.CTkButton(self.scrollable_frame, text = 'People using safely managed sanitation services (% of population)', font = ('Helavetica', 15), command= self.display_sanitation)
        self.sanitation_button.grid(row = 56, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
    def show_fragility(self):
        self.age_button = ctk.CTkButton(self.scrollable_frame, text = 'Age dependency ratio (% of working-age population) ', font = ('Helavetica', 15), command=self.display_age)
        self.age_button.grid(row = 52, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
        self.homicide_button = ctk.CTkButton(self.scrollable_frame, text = 'Intentional homicides (per 100,000 people)', font = ('Helavetica', 15), command=self.display_homicide)
        self.homicide_button.grid(row = 54, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
        self.refugee_button = ctk.CTkButton(self.scrollable_frame, text = 'Refugee population in asylums', font = ('Helavetica', 15), command=self.display_refugee)
        self.refugee_button.grid(row = 56, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)

    def show_environment(self):
        self.forest_button = ctk.CTkButton(self.scrollable_frame, text = ' net forest depletion (% of GNI)', font = ('Helavetica', 15), command=self.display_graph)
        self.forest_button.grid(row = 52, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
        self.freshwater_button = ctk.CTkButton(self.scrollable_frame, text = 'Annual freshwater withdrawals, total (% of internal resources)', font = ('Helavetica', 15), command=self.display_graph)
        self.freshwater_button.grid(row = 54, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)
        self.electricity_button = ctk.CTkButton(self.scrollable_frame, text = 'Access to electricity (% of population)', font = ('Helavetica', 15), command=self.display_graph)
        self.electricity_button.grid(row = 56, column = 1, sticky = 'nsew', padx = 5, pady = 5, rowspan = 2)



    def display_graph_gdp(self):
        title = 'Per Captia GDP of India (1960-2022)'
        list_x= ["1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022"]
        list_y = ["83.0351018240893","85.9697041851008","90.2768689288905","101.31516498136","115.487608356699","119.082475942029","89.7575826115815","96.0463298450023","99.5168361228774","107.182143141928","111.968318177372","118.160528911908","122.612453445976","143.456124984427","163.231615579564","157.929385028241","161.137236080759","186.419089544981","206.073749258556","224.575437698719","267.390578652535","271.426149209154","275.266085855139","292.644647182024","278.095415220662","297.999248705447","312.059843942513","342.071923724964","355.738409768732","347.462029998068","368.749759408129","303.850437957407","317.558738700794","301.50079120851","346.227393115934","373.628235651141","399.577312178982","414.898679748919","412.509354123275","440.961454614021","442.034778911498","449.911124933268","468.844428308942","543.843798895899","624.105094381691","710.509344848758","802.013742049265","1022.73246704551","993.503405266506","1096.63613605519","1350.63447029491","1449.60330101563","1434.01798721629","1438.05700508042","1559.86377870535","1590.17433135955","1714.27953740039","1957.96981329558","1974.3777314935","2050.1638002619","1913.21973278751","2238.12714218765","2410.88802070689"]

        graph = Graph(title, list_x, list_y)
        graph.mainloop()
    def display_graph_inflation(self):
        title = 'Inflation, consumer prices (annual % 1960- 2022)'
        list_x = [1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
        list_y = [1.779877847, 1.695212939, 3.632214971, 2.946161357, 13.35526115, 9.474758592, 10.80184835, 13.06220248, 3.237412426, -0.58413661, 5.09226162, 3.079938684, 6.442097462, 16.94081598, 28.59873408, 5.748430298, -7.633947634, 8.307470092, 2.523048757, 6.275683368, 11.34607348, 13.1125469, 7.890742794, 11.8680813, 8.318907119, 5.556424232, 8.729720727, 8.801125813, 9.383471862, 7.074280029, 8.971232503, 13.87024618, 11.78781704, 6.326890488, 10.24793556, 10.22488616, 8.977152338, 7.164252115, 13.23083898, 4.66982038, 4.00943591, 3.779293122, 4.297152039, 3.805858995, 3.767251735, 4.24634362, 5.796523376, 6.372881356, 8.349267049, 10.88235294, 11.98938992, 8.911793365, 9.478996914, 10.01787847, 6.665656719, 4.906973441, 4.948216341, 3.328173375, 3.938826467, 3.729505735, 6.623436776, 5.131407472, 6.699034141]
        graph = Graph(title, list_x, list_y)
        graph.mainloop()
    def display_graph_une(self):
        title = 'Unemployement, female (% of female labor force)'
        list_x = [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
        list_y = [6.724, 6.724, 6.724, 6.718, 6.921, 7.123, 7.331, 7.538, 7.741, 7.945, 8.151, 8.363, 8.564, 8.765, 8.964, 8.868, 8.772, 8.683, 8.587, 8.49, 8.392, 8.299, 8.205, 8.106, 8.006, 7.907, 7.812, 7.717, 6.075, 6.751, 5.39, 4.586, 3.935]
        graph = Graph(title, list_x, list_y)
        graph.mainloop()
    def display_birth_rate(rate):
        title = 'Birth rate, crude (per 1,000 people)'
        list_x = [1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
        list_y = [42.506, 42.294, 42.101, 41.907, 41.721, 41.346, 40.918, 40.592, 40.207, 39.792, 39.533, 39.43, 39.173, 38.962, 38.629, 37.937, 37.665, 36.89, 36.383, 36.252, 36.214, 36.024, 35.605, 35.3, 35.094, 34.602, 34.483, 33.681, 33.166, 32.549, 31.816, 31.423, 30.914, 30.285, 29.841, 29.361, 28.786, 28.274, 27.784, 27.26, 27.001, 26.728, 26.082, 25.375, 24.728, 23.94, 23.22, 22.713, 22.276, 21.934, 21.438, 20.945, 20.421, 19.935, 19.049, 18.765, 18.514, 17.911, 17.651, 17.049, 16.572, 16.419]
        graph = Graph(title, list_x, list_y)
        graph.mainloop()
    
    def display_hiv(self):
        title = 'Prevalence of HIV, total (% of population ages 15-49)'
        list_x = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
        list_y = [0.1, 0.1, 0.2, 0.2, 0.3, 0.4, 0.4, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
        graph = Graph(title, list_x, list_y)
        graph.mainloop()

    def display_sanitation(self):
        title = 'People using safely managed sanitation services (% of population)'
        list_x = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
        list_y = [6.096392313, 7.399400388, 8.782426344, 10.17746712, 12.56089644, 14.66108933, 16.76951846, 18.96300541, 21.16935265, 23.38820895, 25.6195429, 27.86325391, 30.11935259, 32.38714535, 34.66598361, 36.95517413, 39.25401861, 41.47564339, 43.62501301, 45.76642277, 47.89959768, 50.0241473, 52.1399331]

        graph = Graph(title, list_x, list_y)
        graph.mainloop()

    def display_age(self):
        title = 'Age dependency ratio (% of working-age population) '
        list_x = [1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
        list_y = [77.97427802, 78.97333965, 79.99751809, 81.01273642, 81.64474209, 81.79666486, 81.76475905, 81.59826344, 81.35813691, 81.07479441, 80.72556962, 80.38548167, 80.06327477, 79.7450559, 79.46074039, 79.15337644, 78.82077626, 78.41968483, 77.92428954, 77.4335794, 76.99499961, 76.61424931, 76.23945739, 75.83359284, 75.43863173, 75.05170971, 74.65804987, 74.22579135, 73.71668508, 73.15103192, 72.55431466, 71.95759784, 71.38078271, 70.80648607, 70.18678835, 69.50172819, 68.74888943, 67.95142111, 67.13037766, 66.27117497, 65.40816687, 64.55324323, 63.70378872, 62.85041436, 61.96232145, 61.05733454, 60.12096467, 59.15501643, 58.20561121, 57.28110818, 56.35915817, 55.44659178, 54.55749587, 53.69513485, 52.89442862, 52.14810069, 51.40973408, 50.68482818, 50.01892798, 49.40102931, 48.77554811, 48.12632543, 47.49861638]

        graph = Graph(title, list_x, list_y)
        graph.mainloop()

    def display_homicide(self):
        title = 'Intentional homicides (per 100,000 people)'
        list_x = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
        list_y = [5.073455128, 5.464250011, 5.474814984, 5.175898191, 5.020618843, 4.810432851, 4.770964721, 4.730752602, 4.825761843, 4.592118937, 4.545627523, 4.302247607, 4.164204411, 3.967281189, 4.091476642, 3.905550671, 3.835039683, 3.812920257, 3.811856573, 3.7448918, 3.744921001, 3.788104108, 3.72526295, 3.55331583, 3.62257613, 3.354306716, 3.161426203, 3.028882799, 2.993783858, 2.92666093, 2.911155454, 2.936278893]

        graph = Graph(title, list_x, list_y)
        graph.mainloop()

    def display_refugee(self):
        title = 'Refugee population in asylums'
        list_x = [1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
        list_y = [3510, 5010, 6930, 7200, 6720, 6440, 6720, 6645, 9549, 212743, 210569, 258372, 262802, 258342, 227481, 233371, 223072, 185516, 180031, 170940, 169548, 168853, 164754, 162683, 139284, 158358, 161534, 184539, 185318, 184814, 185118, 185644, 188391, 199931, 201379, 197848, 197142, 195887, 195103, 195373, 212413, 242835]

        graph = Graph(title, list_x, list_y)
        graph.mainloop()

    def display_forest(self):
        title = 'net forest depletion (% of GNI)'
        list_x = [1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
        list_y = [0.412892977, 0.34317677, 0.332986901, 0.477874242, 0.491996934, 1.073210036, 0.681242876, 1.817336696, 1.621190427, 0.674075291, 0.663076618, 0.56985755, 0.837339019, 0.538922661, 0.469239658, 0.315767129, 0.537981343, 0.447544247, 0.448165585, 0.448210193, 0.544712344, 0.633772394, 0.619983102, 0.629014498, 0.455473016, 0.495177822, 0.422706188, 0.382143609, 0.365723081, 0.388545336, 0.342973266, 0.331096696, 0.37417915, 0.341818488, 0.24451664, 0.213464418, 0.284269162, 0.303026557, 0.30110295, 0.260759906, 0.380636441, 0.354732294, 0.313210382, 0.283202329, 0.268202532, 0.298467427, 0.304148826, 0.209054527, 0.150445691, 0.157402582, 0.188802021, 0.163266862]
        graph = Graph(title, list_x, list_y)
        graph.mainloop()
    def display_freshwater(self):
        title = 'Annual freshwater withdrawals, total (% of internal resources)'
        list_x =  [1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
        list_y = [26.27939142, 27.08644537, 27.89349931, 28.70055325, 29.50760719, 30.31466113, 31.12171508, 31.92876902, 32.73582296, 33.5428769, 34.34993084, 34.395574, 34.44121715, 34.4868603, 34.53250346, 34.57814661, 35.34162863, 36.10511065, 36.86859267, 37.63207469, 38.39555671, 39.15903873, 39.92251037, 40.68599585, 41.44948479, 42.2129668, 43.25445989, 44.29595297, 45.33744606, 43.23926003, 43.49583333, 43.75240664, 44.00897994, 44.26555325, 44.52212656, 44.77869986, 44.77869986, 44.77869986, 44.77869986, 44.77869986, 44.77869986, 44.77869986, 44.77869986, 44.77869986, 44.77869986, 44.77869986]

        graph = Graph(title, list_x, list_y)
        graph.mainloop()
    def display_electricity(self):
        title = 'Access to electricity (% of population)'
        list_x = [1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
        list_y = [50.9, 49.81130981, 51.40877533, 53.00352097, 54.59486389, 56.18213272, 60.1, 60.29283905, 62.00543976, 62.3, 65.41201019, 64.4, 68.8404541, 67.9, 72.3407135, 74.11849213, 75, 76.3, 79.51678467, 79.9, 83.13139343, 85.13391113, 88, 89.58630371, 91.79415894, 95.7, 95.88594055, 96.5, 99.57252502]

        graph = Graph(title, list_x, list_y)
        graph.mainloop()   

    def dashboard(self):
        email = self.email_address
        login_number = self.login_number
        print("Infographics Page: ", login_number, email)
        self.destroy()
        news_app = Dashboard(None, login_number, email)
        news_app.mainloop()

    def search_news(self):
        self.destroy()
        search_app = SearchEmail(self.email_id, self.login_number)
        search_app.mainloop()

    def news_by_category(self):
        self.destroy()
        news_app = NewsCategory(self.email_id, self.login_number)
        news_app.mainloop()


    
    def loginPage(self):
        self.destroy()
        App().mainloop()

    def profile(self):
        self.destroy()
        print(self.login_number)
        news_app = NewsAppDashboardProfile(self.login_number)
        news_app.mainloop()


class Graph(tk.Tk):
    def __init__(self, title, list_x, list_y):
        super().__init__()
        self.text = title
        self.title(self.text)
        self.list_x= list_x
        self.list_y = list_y

        self.plot_types = ['Line Plot', 'Bar Plot', 'Scatter Plot']
        self.plot_type_var = tk.StringVar(value=self.plot_types[0])
        self.plot_menu = tk.OptionMenu(self, self.plot_type_var, *self.plot_types, command=self.plot_type_select)
        self.plot_menu.pack(padx=10, pady=10)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.axes = self.figure.add_subplot()

        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.load_button = tk.Button(self, text='Load Graph', command=self.load_data)
        self.load_button.pack(padx=5, pady=5)


        NavigationToolbar2Tk(self.figure_canvas, self)

    def load_data(self):
        self.x_values = [int(i) for i in self.list_x]
        self.y_values = [float(i) for i in self.list_y]
        self.plot_type_select()

    def plot_type_select(self, event = None):
        self.axes.clear()  
        plot_type = self.plot_type_var.get()
        if plot_type == 'Line Plot':
            self.axes.plot(self.x_values, self.y_values)
        elif plot_type == 'Bar Plot':
            self.axes.bar(self.x_values, self.y_values)
        elif plot_type == 'Scatter Plot':
            self.axes.scatter(self.x_values, self.y_values)
        self.axes.set_title(self.text)
        self.axes.set_ylabel(' Percentage %')
        self.axes.set_xlabel('Years')
  
        self.figure_canvas.draw()


if __name__ == "__main__":
    App().mainloop()