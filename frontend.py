import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

import backend as backend

selected_tuple = ()

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.title("Tournament")
        self.geometry("1000x800")

        container = ttk.Frame(self)
        container.grid(padx=10, pady=10, sticky="EW")

        self.frames = dict()
        for FrameClass in (MainMenu, Competitors, Events, Leaderboards, Activities, Admin):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
        print(self.frames)

        self.show_frame(MainMenu)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class MainMenu(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        # Header Label
        lblMainMenu = ttk.Label(self, text="Main Menu")
        lblMainMenu.grid(row=0, column=0, sticky="EW")

        button_text = [Competitors, Events, Leaderboards, Activities, Admin]
        for i in range(len(button_text)):
            button = ttk.Button(self, text=button_text[i].__name__, width=15, command=lambda i=i: controller.show_frame(button_text[i]))
            button.grid(row=i, column=1, padx=10, pady=15)

        exit_button = ttk.Button(self, text="Exit", width=15, command=lambda: exit())
        exit_button.grid(row=i, column=1, padx=10, pady=15)

        # image


class Competitors(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=0)

        self.Forename_text = tk.StringVar()
        self.Surname_text = tk.StringVar()
        self.Team_Name_text = tk.StringVar()
        self.Competitor_ID_text = tk.StringVar()
        self.Competitor_Type_ID_text = tk.StringVar()

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=0, column=1, ipadx=5, ipady=5, padx=10, pady=10, sticky='n')
        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.grid(row=0, column=0, sticky='EW')
        self.data_entry_frame = ttk.Frame(self.content_frame)
        self.data_entry_frame.grid(row=1, column=0)
        self.Listbox_frame = ttk.Frame(self.content_frame)
        self.Listbox_frame.grid(row=2, column=0, sticky='NS')

        # Header Label
        ttk.Label(self.header_frame, text="Competitors", font=("verdana", 22, 'bold'), foreground="red").grid(row=0, column=1, sticky="w")

        # data entry labels

        label_text = ['Forename', 'Surname', 'Team Name', 'Competitor ID', 'Competitor Type ID']

        for i in range(len(label_text)):
            ttk.Label(self.data_entry_frame, text=label_text[i] + ":").grid(row=i, column=0, padx=5, pady=5, sticky="w")

        # Data entry buttons

        self.entry_Forename = ttk.Entry(self.data_entry_frame, textvariable=self.Forename_text, width=15).grid(row=0, column=6, padx=15, pady=1)
        self.entry_Surname = ttk.Entry(self.data_entry_frame, textvariable=self.Surname_text, width=15).grid(row=1, column=6, padx=15, pady=1)
        self.entry_Team_Name = ttk.Entry(self.data_entry_frame, textvariable=self.Team_Name_text, width=15).grid(row=2, column=6, padx=15, pady=1)
        self.entry_Competitor_ID = ttk.Entry(self.data_entry_frame, textvariable=self.Competitor_ID_text, width=15).grid(row=3, column=6, padx=15, pady=1)
        self.entry_Competitor_Type_ID = ttk.Entry(self.data_entry_frame, textvariable=self.Competitor_Type_ID_text, width=15).grid(row=4, column=6, padx=15, pady=1)

        # List box
        self.lstResults = tk.Listbox(self.Listbox_frame, width=60)
        self.lstResults.grid(row=0, column=0, padx=5, pady=5)

        # scroll bar
        self.scb_lstResults = ttk.Scrollbar(self.Listbox_frame)
        self.scb_lstResults.grid(row=0, column=1, sticky='ns')

        self.lstResults.configure(yscrollcommand=self.scb_lstResults.set)
        self.scb_lstResults.config(command=self.lstResults.yview)

        self.scb_lstResults.bind('<<listboxSelect>>', self.get_selected_row)

        # Buttons frame

        text = ['View All', 'Search', 'Add', 'Update Selected', 'Delete Selected', 'Main Menu']
        functions = [self.view_all_command, self.competitor_search_command, self.add_command, self.update_command, self.delete_command, lambda: controller.show_frame(MainMenu)]
        for i in range(len(text)):
            button = ttk.Button(self.buttons_frame, text=text[i], width=14, command=functions[i])
            button.grid(row=i + 1, column=0, padx=5, pady=10, sticky='n')

    def view_all_command(self):
        self.lstResults.delete(0, 'end')
        for row in backend.view_all_competitors():
            self.lstResults.insert('end', row)

    def get_selected_row(self, event):
        try:
            global selected_tuple
            self.lstResults.curselection()
            print(selected_tuple)
            self.entry_Forename.delete(0, 'end')
            self.entry_Forename.insert('end', selected_tuple[1])
            self.entry_Surname.delete(0, 'end')
            self.entry_Surname.insert('end', selected_tuple[2])
            self.entry_Team_Name.delete(0, 'end')
            self.entry_Team_Name.insert('end', selected_tuple[3])
            self.entry_Competitor_Type_ID.delete(0, 'end')
            self.entry_Competitor_Type_ID.insert('end', selected_tuple[4])
            self.entry_Competitor_ID.delete(0, 'end')
            self.entry_Competitor_ID.insert('end', selected_tuple[0])
        except IndexError:
            pass

    def competitor_search_command(self):
        self.lstResults.delete(0, 'end')
        for row in backend.competitor_search(self.Forename_text.get(), self.Surname_text.get(),
                                             self.Team_Name_text.get(), self.Competitor_ID_text.get(), self.Competitor_ID_text.get()):
            self.lstResults.insert('end', row)

    def add_command(self):
        backend.insert_competitor(self.Forename_text.get(), self.Surname_text.get(), self.Team_Name_text.get(), int(self.Competitor_ID_text.get()), int(self.Competitor_Type_ID_text.get()))
        self.lstResults.delete(0, 'end')
        self.lstResults.insert('end', (self.Forename_text.get(), self.Surname_text.get(), self.Competitor_ID_text.get(), self.Competitor_Type_ID_text.get()))

    def update_command(self):
        print(selected_tuple[0], self.Forename_text.get(), self.Surname_text.get(), self.Team_Name_text.get(), self.Competitor_ID_text.get(), self.Competitor_Type_ID_text.get())
        print(selected_tuple[0])
        backend.update_competitor(selected_tuple[0], self.Forename_text.get(), self.Surname_text.get(), self.Competitor_Type_ID_text.get(), self.Competitor_ID_text.get(), self.Competitor_Type_ID_text.get())

    def delete_command(self):
        backend.delete_competitor(selected_tuple[0])
        self.lstResults.delete(0, 'end')
        for row in backend.competitors_view_all():
            self.lstResults.insert('end', row)


class Events(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.event_id_text = tk.StringVar()
        self.competitor_id_text = tk.StringVar()
        self.activity_id_text = tk.StringVar()
        self.score_id_text = tk.StringVar()
        self.date_text = tk.StringVar()
        self.event_type_text = tk.StringVar()

        # layout frames

        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=0)
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=0, column=1, ipadx=5, ipady=5, padx=10, pady=10)
        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.grid(row=0, column=0, sticky='ew')
        self.data_entry_frame = ttk.Frame(self.content_frame)
        self.data_entry_frame.grid(row=1, column=0)
        self.listbox_frame = ttk.Frame(self.content_frame)
        self.listbox_frame.grid(row=2, column=0, sticky='ns')

        # header section
        ttk.Label(self.header_frame, text='Events', font=('monsterrat', 22, 'bold'), foreground='blue').grid(row=0, column=1, sticky='W')

        # data entry section - labels

        label_text = ['Event', 'Competitor ID', 'Activity ID', 'Score', 'Date', 'Event ID']

        for i in range(len(label_text)):
            ttk.Label(self.data_entry_frame, text=label_text[i] + ":").grid(row=i, column=0, padx=5, pady=5, sticky="w")

        # data entry section - entry buttons
        self.entry_eventID = ttk.Entry(self.data_entry_frame, textvariable=self.event_id_text, width=15).grid(row=0, column=1, padx=0, pady=0)
        self.entry_Competitor_ID = ttk.Entry(self.data_entry_frame, textvariable=self.competitor_id_text, width=15).grid(row=1, column=1, padx=0, pady=0)
        self.entry_activityID = ttk.Entry(self.data_entry_frame, textvariable=self.activity_id_text, width=15).grid(row=2, column=1, padx=0, pady=0)
        self.entry_ScoreID = ttk.Entry(self.data_entry_frame, textvariable=self.score_id_text, width=15).grid(row=3, column=1, padx=0, pady=0)
        self.entry_date = ttk.Entry(self.data_entry_frame, textvariable=self.date_text, width=15).grid(row=4, column=1, padx=0, pady=0)
        self.entry_event_type = ttk.Entry(self.data_entry_frame, textvariable=self.event_type_text, width=15).grid(row=5, column=1, padx=0, pady=0)

        # list box
        self.lstResults = tk.Listbox(self.listbox_frame, width=60)
        self.lstResults.grid(row=0, column=6, padx=0, pady=0)

        # scroll bar for list box
        self.scb_lstResults = ttk.Scrollbar(self.listbox_frame)
        self.scb_lstResults.grid(row=0, column=7, sticky='ns')

        self.lstResults.configure(yscrollcommand=self.scb_lstResults.set)
        self.scb_lstResults.config(command=self.lstResults.yview)

        self.scb_lstResults.bind('<<listboxSelect>>', self.event_get_selected_row)

        # buttons frame:

        button_text = ['View All', 'Search', 'Add', 'Update Selected', 'Delete Selected', 'Main Menu']
        button_functions = [self.event_view_all_command, self.event_search_command, self.event_add_command, self.event_update_command, self.event_delete_command, lambda: controller.show_frame(MainMenu)]
        for i in range(len(button_text)):
            button = ttk.Button(self.buttons_frame, text=button_text[i], width=14, command=button_functions[i])
            button.grid(row=i, column=2, padx=5, pady=5, sticky='n')

    def event_view_all_command(self):
        self.lstResults.delete(0, 'end')
        for row in backend.events_view_all():
            self.lstResults.insert('end', row)

    def event_get_selected_row(self):
        try:
            global selected_tuple
            index = self.lstResults.curselection()[0]
            selected_tuple = self.lstResults.get(index)
            entry_removal = [self.entry_eventID, self.entry_activityID, self.entry_Competitor_ID, self.entry_ScoreID, self.entry_eventID]

            for i in range(len(entry_removal)):
                entry_removal[i].delete(0, 'end')
                entry_removal[i].insert('end', selected_tuple[i])

            # Find a way to test this
            '''
            self.entry_eventID.delete(0, 'end')
            self.entry_eventID.insert('end', selected_tuple[0])
            self.entry_activityID.delete(0, 'end')
            self.entry_activityID.insert('end', selected_tuple[1])
            self.entry_Competitor_ID.delete(0, 'end')
            self.entry_Competitor_ID.insert('end', selected_tuple[2])
            self.entry_ScoreID.delete(0, 'end')
            self.entry_ScoreID.insert('end', selected_tuple[3])
            self.entry_eventID.delete(0, 'end')
            self.entry_eventID.insert('end', selected_tuple[3])
            '''
        except IndexError:
            pass

    def event_search_command(self):
        self.lstResults.delete(0, 'end')
        for row in backend.event_search(self.event_id_text.get(), self.activity_id_text.get(), self.competitor_id_text.get(), self.score_id_text.get(), self.date_text.get(), self.event_type_text.get()):
            self.lstResults.insert('end', row)

    def event_add_command(self):
        backend.insert_events(self.event_id_text.get(), self.activity_id_text.get(), int(self.competitor_id_text.get()), int(self.score_id_text.get()), self.date_text.get(), self.event_type_text.get())
        self.lstResults.delete(0, 'end')
        self.lstResults.insert('end', (self.event_id_text.get(), self.activity_id_text.get(), int(self.competitor_id_text.get()), int(self.score_id_text.get()), self.date_text.get(), self.event_type_text.get()))
        for row in backend.events_view_all():
            self.lstResults.insert('end', row)

    def event_update_command(self):
        backend.update_events(selected_tuple[0], self.activity_id_text.get(), self.competitor_id_text.get(), self.score_id_text.get(), self.date_text.get(), self.event_type_text.get())

    def event_delete_command(self):
        print("Yas queen slay")
        self.lstResults.delete(0, 'end')
        for row in backend.delete_event(selected_tuple[0]):
            self.lstResults.insert('end', row)


class Leaderboards(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        # Layout Frames
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=0)

        self.buttons_frame = ttk.Frame(self.content_frame)
        self.content_frame.grid(row=0, column=1, ipadx=5, ipady=5, padx=10, pady=10, sticky='n')

        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.grid(row=0, column=2, ipadx=5, ipady=5, padx=10, pady=10, sticky='n')

        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=0, column=3, ipadx=5, ipady=5, padx=10, pady=10, sticky='n')

        # Header section

        lblTitle = ttk.Label(self, text="Leaderboards")
        lblTitle.grid(row=0, column=0)

        # Listbox
        self.lstResults = tk.Listbox(self.listbox_frame, width=60)
        self.lstResults.grid(row=0, column=0, padx=5, pady=5)
        self.listbox_frame.grid(row=2, column=0, sticky='NS')  # found the error

        # scroll bar

        self.scb_lstResults = ttk.Scrollbar(self.listbox_frame)
        self.scb_lstResults.grid(row=0, column=1, sticky='ns')

        self.lstResults.configure(yscrollcommand=self.scb_lstResults.set)
        self.scb_lstResults.config(command=self.lstResults.yview)

        # buttons frame

        ttk.Label(self.header_frame, text="Leaderboards", anchor="w").grid(row=0, column=0, sticky="w")

        self.lstResults = tk.Listbox(self.listbox_frame, width=60)
        self.lstResults.grid(row=0, column=0, padx=5, pady=5)

        self.scb_lstResults = ttk.Scrollbar(self.listbox_frame)
        self.scb_lstResults.grid(row=0, column=1, sticky="NS")

        self.lstResults.configure(yscrollcommand=self.scb_lstResults.set)
        self.scb_lstResults.config(command=self.lstResults.yview)

        button_text = ['Individual Single Event', 'Individual Multiple Events', 'Team Single Event', 'Team Multiple Event', 'Main Menu']
        button_functions = [self.individual_single, self.individual_multiple, self.team_single, self.team_multiple, lambda: controller.show_frame(MainMenu)]
        for i in range(len(button_text)):
            button = ttk.Button(self.buttons_frame, text=button_text[i], width=16, command=button_functions[i])
            button.grid(row=i, column=0, padx=5, pady=10, sticky="n")

    def individual_single(self):
        self.lstResults.delete(0, 'end')
        for row in backend.individual_single_leaderboard():
            self.lstResults.insert('end', row)
        print("Individual_single_leaderboard")

    def individual_multiple(self):
        self.lstResults.delete(0, 'end')
        for row in backend.individual_multi_leaderboard():
            self.lstResults.insert('end', row)
        print("Individual_multi_leaderboard")

    def team_single(self):
        self.lstResults.delete(0, 'end')
        for row in backend.team_single_leaderboard():
            self.lstResults.insert('end', row)
        print("Team_single_leaderboard")

    def team_multiple(self):
        self.lstResults.delete(0, 'end')
        for row in backend.team_multi_leaderboard():
            self.lstResults.insert('end', row)
        print("team_multi_leaderboard")


class Activities(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        lblTitle = ttk.Label(self, text="Activities")
        lblTitle.grid(row=0, column=0)

        self.activity_id_text = tk.StringVar()
        self.activity_description_text = tk.StringVar()

        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=0)

        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.grid(row=0, column=0)

        ttk.Label(self.header_frame, text="Activities", anchor="w").grid(row=0, column=0, sticky="w")

        self.buttons_frame = ttk.Frame(self.content_frame)
        self.buttons_frame.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=0, sticky="n")

        self.data_entry_frame = ttk.Frame(self.content_frame)
        self.data_entry_frame.grid(row=1, column=0)

        self.listbox_frame = ttk.Frame(self.content_frame)
        self.listbox_frame.grid(row=2, column=0, sticky="EW")

        self.lstResults = tk.Listbox(self.listbox_frame, width=60)
        self.lstResults.grid(row=0, column=0, padx=5, pady=5)

        self.scb_lstResults = ttk.Scrollbar(self.listbox_frame)
        self.scb_lstResults.grid(row=0, column=1, sticky="NS")

        self.lstResults.configure(yscrollcommand=self.scb_lstResults.set)
        self.scb_lstResults.config(command=self.lstResults.yview)

        button_text = ['View All', 'Search', 'Add', 'Update Selected', 'Delete Selected', 'Main Menu']
        button_functions = [self.view_all_command, self.search_command, self.add_command, self.update_command, self.delete_command, lambda: controller.show_frame(MainMenu)]
        for i in range(len(button_text)):
            button = ttk.Button(self.buttons_frame, text=button_text[i], width=14, command=button_functions[i])
            button.grid(row=i, column=2, padx=5, pady=5, sticky='n')

    def update_command(self):
        backend.update_events(selected_tuple[0], self.activity_de_text.get(), self.competitor_id_text.get(), self.score_id_text.get(), self.date_text.get(), self.event_type_text.get())

    def view_all_command(self):
        self.lstResults.delete(0, 'end')
        for row in backend.activity_view_all():
            self.lstResults.insert('end', row)

    def get_selected_row(self):
        try:
            global selected_tuple
            index = self.lstResults.curselection()[0]
            selected_tuple = self.lstResults.get(index)
            entry_removal = [self.entry_eventID, self.entry_activityID, self.entry_Competitor_ID, self.entry_ScoreID, self.entry_eventID]

            for i in range(len(entry_removal)):
                entry_removal[i].delete(0, 'end')
                entry_removal[i].insert('end', selected_tuple[i])
        except IndexError:
            pass

    def search_command(self):
        self.lstResults.delete(0, 'end')
        for row in backend.activity_search(self.event_id_text.get(), self.activity_id_text.get(), self.competitor_id_text.get(), self.score_id_text.get(), self.date_text.get(), self.event_type_text.get()):
            self.lstResults.insert('end', row)

    def add_command(self):
        backend.insert_activity(int(self.activity_id_text.get()), self.activity_description_text.get())
        self.lstResults.delete(0, 'end')
        self.lstResults.insert('end', (self.activity_id_text.get(), self.activity_id_text.get(), int(self.activity_description_text.get())))

    def delete_command(self):
        self.lstResults.delete(0, 'end')
        for row in backend.delete_activity(selected_tuple[0]):
            self.lstResults.insert('end', row)

class Admin(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        lblTitle = ttk.Label(self, text="Admin")
        lblTitle.grid(row=0, column=0)

        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=0)

        self.buttons_frame = ttk.Frame(self.content_frame)
        self.buttons_frame.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=0, sticky="n")

        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.grid(row=0, column=2, sticky="EW")

        self.body_frame = ttk.Frame(self.content_frame)
        self.body_frame.grid(row=1, column=3, sticky="EW")

        # Title header

        ttk.Label(self.header_frame, text="Administration", font=("montserrat", 22, 'bold', 'underline'), foreground="blue").grid(row=0, column=1, sticky="w")

        # Insert Image Here

        button_text = ['Backup database', 'Delete Tables', 'Main Menu']
        button_functions = [self.delete_database, self.delete_tables, lambda: controller.show_frame(MainMenu)]
        for i in range(len(button_text)):
            button = ttk.Button(self.buttons_frame, text=button_text[i], width=16, command=button_functions[i])
            button.grid(row=i, column=0, padx=5, pady=10, sticky="n")

    def backup_database(self):
        backend.backup_database(self)

    def delete_database(self):
        backend.delete_database(self)

    def delete_tables(self):
        backend.drop_tables(self)

    def copy_database(self):
        backend.copy_database


root = App()
root.mainloop()
