import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

class WebInfoExtractorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("~ContentCrawler~")

        # Load app logo
        self.load_logo()

        self.create_widgets()

    def load_logo(self):
        try:
            logo_path = "Your Logo path"
            img = Image.open(logo_path)
            img = img.resize((100, 100), Image.BILINEAR)
            self.logo_image = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            self.logo_image = None
            print("Logo file not found. Please provide a valid path.")

    def create_widgets(self):
        # Style for setting background color
        style = ttk.Style()
        style.configure("TFrame", background='#f0f0fa')

        # Main frame
        self.main_frame = ttk.Frame(self.master, padding="10", style="TFrame")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Logo and App Name
        if self.logo_image:
            logo_label = ttk.Label(self.main_frame, image=self.logo_image)
            logo_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        app_name_label = ttk.Label(self.main_frame, text="~Content Crawler~", font=("Helvetica", 20, "bold"), background="#b1b7bd")
        app_name_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Entry for URL input
        self.url_entry = ttk.Entry(self.main_frame, width=40, background="#b1b7bd")
        self.url_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Button to fetch data
        self.fetch_button = ttk.Button(self.main_frame, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.grid(row=1, column=2, padx=5, pady=5)

        # Notebook for multiple screens
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title tab
        self.title_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.title_tab, text="Title")

        # Meta Information tab
        self.meta_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.meta_tab, text="Meta Information")

        # Article Description tab
        self.description_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.description_tab, text="Article Description")

        # Summary tab
        self.summary_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_tab, text="Summary")

        # Labels to display information with text wrap
        label_style = ttk.Style()
        label_style.configure("WrapLabel.TLabel", font=("Helvetica",16, "bold"), background="#b1b7bd", wraplength=600)
        
        self.title_label = ttk.Label(self.title_tab, text="Title:", style="WrapLabel.TLabel")
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.meta_label = ttk.Label(self.meta_tab, text="Meta Information:", style="WrapLabel.TLabel")
        self.meta_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.description_label = ttk.Label(self.description_tab, text="Article Description:", style="WrapLabel.TLabel")
        self.description_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.summary_label = ttk.Label(self.summary_tab, text="Summary:", style="WrapLabel.TLabel")
        self.summary_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    def fetch_data(self):
        url = self.url_entry.get()
        if url:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract title
                title = soup.title.string if soup.title else "Title not found"

                # Extract meta information
                meta_info = "\n".join([str(tag) for tag in soup.find_all('meta')])

                
                 # Extract article description
                content_div = soup.find('div', {'class': 'mw-parser-output'})
                description_paragraph = content_div.find_all('p') if content_div else None
                #description = description_paragraph.text if description_paragraph else "Description not found"
                if description_paragraph and len(description_paragraph) > 2:
                    description = description_paragraph[2].text
                else:
                    summary = "description not found"

                # Extract summary from the main content (second paragraph)
                summary_paragraphs = content_div.find_all('p') if content_div else None

                # Check if there is a second paragraph
                if summary_paragraphs and len(summary_paragraphs) > 1:
                    summary = summary_paragraphs[1].text
                else:
                    summary = "Summary not found"
                # Update labels with scraped data
                self.title_label.config(text=f"Title: {title}")
                self.meta_label.config(text=f"Meta Information:\n{meta_info}")
                self.description_label.config(text=f"Article Description: {description}")
                self.summary_label.config(text=f"Summary: {summary}")

            except requests.RequestException as e:
                print(f"Error fetching data: {e}")
        else:
            print("Please enter a valid URL")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebInfoExtractorApp(root)
    root.mainloop()

