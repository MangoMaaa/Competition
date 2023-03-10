import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageFont, ImageDraw

import backend as backend

selected_tuple = ()


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.title("Tournament")
        self.geometry("800x655")

        container = ttk.Frame(self)
        container.grid(padx=10, pady=10, sticky="EW")

        self.frames = dict()
        for FrameClass in (MainMenu, Competitors, Events, Leaderboards, Activities, Admin):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=1, column=0, sticky="NSEW")
        print(self.frames)

        self.show_frame(MainMenu)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


def layout_frames(self):
    self.content_frame = ttk.Frame(self)
    self.content_frame.grid(row=0, column=0)

    self.buttons_frame = ttk.Frame(self.content_frame)
    self.buttons_frame.grid(row=1, column=0, ipadx=5, ipady=5, padx=10, pady=40)

    self.header_frame = ttk.Frame(self.content_frame)
    self.header_frame.grid(row=0, column=2, sticky='ew')

    self.data_entry_frame = ttk.Frame(self.content_frame)
    self.data_entry_frame.grid(row=1, column=2, padx=85, ipady=35)

    self.listbox_frame = ttk.Frame(self.content_frame)
    self.listbox_frame.grid(row=1, column=2, columnspan=10, rowspan=50, padx=100, pady=200, ipady=0, sticky='N')


def create_labels(*text):
    for i in range(len(text)):
        if i + 1 == len(text):
            break

        ttk.Label(text[len(text)-1].data_entry_frame, text=f"{text[i]}:").grid(row=i+1, column=0, padx=5, pady=5, sticky="S")


def create_buttons(*text):
    try:
        for i in range(0, len(text), 2):
            button = ttk.Button(text[len(text)-1].buttons_frame, text=text[i], width=20, command=text[i + 1])
            button.grid(row=2+i, column=0, padx=5, pady=5, sticky='NWS')
    except IndexError:
        return


def insert_image(imageName, sf, imageWidth, imageHeight):
    sport_equipment = Image.open(imageName)
    resized_img = sport_equipment.resize((imageWidth, imageHeight), Image.Resampling.LANCZOS)
    sport_equipment = ImageTk.PhotoImage(resized_img)
    sport_img = ttk.Label(sf, image=sport_equipment)
    sport_img.image = sport_equipment
    sport_img.grid(row=2, columnspan=200, column=0)


def create_scrollbar(self):
    self.lstResults = tk.Listbox(self.listbox_frame, width=60)
    self.lstResults.grid(row=0, column=0, padx=1, pady=5)

    self.scb_lstResults = ttk.Scrollbar(self.listbox_frame)
    self.scb_lstResults.grid(row=0, column=1, sticky="NS")

    self.lstResults.configure(yscrollcommand=self.scb_lstResults.set)
    self.scb_lstResults.config(command=self.lstResults.yview)


class MainMenu(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        # Header Label
        lblMainMenu = ttk.Label(self, text="Main Menu", font=("verdana", 22, 'bold'), foreground="#6225da")
        lblMainMenu.grid(row=0, column=1, columnspan=3, sticky="SEW")

        button_text = [Competitors, Events, Leaderboards, Activities, Admin]
        for i in range(len(button_text)):
            button = ttk.Button(self, text=button_text[i].__name__, width=15, command=lambda i=i: controller.show_frame(button_text[i]))
            button.grid(row=1, column=i+1, padx=10, pady=10, sticky='EW')

        exit_button = ttk.Button(self, text="Exit", width=15, command=lambda: exit())
        exit_button.grid(row=1, column=i+2, padx=10, pady=15)

        # image
        insert_image("sport equipment.jpg", self, 550, 300)


class Competitors(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        layout_frames(self)

        ttk.Label(self.header_frame, text="Competitors", font=("verdana", 22, 'bold'), foreground="#6225da").grid(row=0, column=0, sticky='NW')

        self.Forename_text = tk.StringVar()
        self.Surname_text = tk.StringVar()
        self.Team_Name_text = tk.StringVar()
        self.Competitor_ID_text = tk.StringVar()
        self.Competitor_Type_ID_text = tk.StringVar()

        # data entry labels
        create_labels('Forename', 'Surname', 'Team Name', 'Competitor ID', 'Competitor Type ID', self)
        # Data entry buttons

        self.entry_Forename = ttk.Entry(self.data_entry_frame, textvariable=self.Forename_text, width=15)\
            .grid(row=1, column=3, padx=5, pady=1)
        self.entry_Surname = ttk.Entry(self.data_entry_frame, textvariable=self.Surname_text, width=15)\
            .grid(row=2, column=3, padx=15, pady=1)
        self.entry_Team_Name = ttk.Entry(self.data_entry_frame, textvariable=self.Team_Name_text, width=15)\
            .grid(row=3, column=3, padx=15, pady=1)
        self.entry_Competitor_ID = ttk.Entry(self.data_entry_frame, textvariable=self.Competitor_ID_text, width=15)\
            .grid(row=4, column=3, padx=15, pady=1)
        self.entry_Competitor_Type_ID = ttk.Entry(self.data_entry_frame, textvariable=self.Competitor_Type_ID_text, width=15)\
            .grid(row=5, column=3, padx=15, pady=1)

        create_scrollbar(self)

        self.scb_lstResults.bind('<<listboxSelect>>', self.get_selected_row)

        # Buttons frame

        create_buttons('View All', self.view_all_command, 'Search', self.competitor_search, 'Add', self.add_command, 'Update Selected', self.update_command, 'Delete Selected', self.delete_competitor, 'Main Menu', lambda: controller.show_frame(MainMenu), self)

    def view_all_command(self):
        self.lstResults.delete(0, 'end')
        for row in backend.view_all_competitors():
            self.lstResults.insert('end', row)

    def get_selected_row(self, event):
        try:
            global selected_tuple
            self.lstResults.curselection()
            print(selected_tuple)
            entry_removal = [self.entry_Competitor_ID, self.entry_Forename, self.entry_Surname, self.entry_Team_Name, self.Competitor_Type_ID]
            for i in range(len(entry_removal)):
                entry_removal[i].delete(0, 'end')
                entry_removal[i].insert('end', selected_tuple[i])
        except IndexError:
            pass

    def competitor_search(self):
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

    def delete_competitor(self):
        backend.delete_competitor(selected_tuple[0])
        self.lstResults.delete(0, 'end')
        for row in backend.view_all_competitors():
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

        layout_frames(self)

        # header section
        ttk.Label(self.header_frame, text='Events', font=('monsterrat', 22, 'bold'), foreground='#6225da').grid(row=0, column=1, sticky='W')

        # data entry section - labels

        create_labels('Event', 'Competitor ID', 'Activity ID', 'Score', 'Date', 'Event ID',self)

        # data entry section - entry buttons
        self.entry_eventID = ttk.Entry(self.data_entry_frame, textvariable=self.event_id_text, width=15).grid(row=1, column=1, padx=0, pady=0)
        self.entry_Competitor_ID = ttk.Entry(self.data_entry_frame, textvariable=self.competitor_id_text, width=15).grid(row=2, column=1, padx=0, pady=0)
        self.entry_activityID = ttk.Entry(self.data_entry_frame, textvariable=self.activity_id_text, width=15).grid(row=3, column=1, padx=0, pady=0)
        self.entry_ScoreID = ttk.Entry(self.data_entry_frame, textvariable=self.score_id_text, width=15).grid(row=4, column=1, padx=0, pady=0)
        self.entry_date = ttk.Entry(self.data_entry_frame, textvariable=self.date_text, width=15).grid(row=5, column=1, padx=0, pady=0)
        self.entry_event_type = ttk.Entry(self.data_entry_frame, textvariable=self.event_type_text, width=15).grid(row=6, column=1, padx=0, pady=0)

        create_scrollbar(self)

        self.scb_lstResults.bind('<<listboxSelect>>', self.event_get_selected_row)

        # buttons frame:

        create_buttons('View All', self.event_view_all_command, 'Search', self.event_search_command, 'Add', self.event_add_command, 'Update Selected', self.event_update_command, 'Delete Selected', self.event_delete_command, 'Main Menu', lambda: controller.show_frame(MainMenu), self)

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
        layout_frames(self)

        # Header section

        ttk.Label(self.header_frame, text='Leaderboards', font=('monsterrat', 22, 'bold'), foreground='#6225da').grid(row=0, column=1, sticky='W')

        # scroll bar

        create_scrollbar(self)

        # buttons frame
        create_buttons('View All', self.contestant_view_all, 'View All Solo', self.view_all_solo, 'View Single Team', self.view_all_one_team,'View All Teams', self.view_all_teams, 'Main Menu', lambda: controller.show_frame(MainMenu), self)

    def contestant_view_all(self):
        self.lstResults.delete(0, 'end')
        for row in backend.contestant_view_all():
            self.lstResults.insert('end', row)
        print("Individual_single_leaderboard")

    def view_all_solo(self):
        self.lstResults.delete(0, 'end')
        for row in backend.view_all_solo():
            self.lstResults.insert('end', row)
        print("Individual_multi_leaderboard")

    def view_all_one_team(self):
        self.lstResults.delete(0, 'end')
        for row in backend.view_all_one_team():
            self.lstResults.insert('end', row)
        print("Team_single_leaderboard")

    def view_all_teams(self):
        self.lstResults.delete(0, 'end')
        for row in backend.view_all_teams():
            self.lstResults.insert('end', row)
        print("team_multi_leaderboard")


class Activities(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        lblTitle = ttk.Label(self, text="Activities")
        lblTitle.grid(row=0, column=0)

        self.activity_id_text = tk.StringVar()
        self.activity_description_text = tk.StringVar()

        # layout frames
        layout_frames(self)

        # title
        ttk.Label(self.header_frame, text='Activities', font=('monsterrat', 22, 'bold'), foreground='#6225da').grid(row=0, column=1, sticky='W')

        # scrollbar
        create_scrollbar(self)

        # image
        insert_image("Neco-Arc_Remake (1).png", self, 3, 5)

        # entry section
        self.entry_activityID = ttk.Entry(self.data_entry_frame, textvariable=self.activity_id_text, width=15).grid(row=1, column=1, padx=0, pady=0, sticky='N')
        self.entry_activity = ttk.Entry(self.data_entry_frame, textvariable=self.activity_description_text, width=15).grid(row=2, column=1, padx=0, pady=0, sticky='S')

        # entry section labels
        create_labels("Activity ID", "Activity Name", self)

        create_buttons('View All', self.view_all_command, 'Search', self.search_command, 'Add', self.add_command, 'Update Selected', self.update_command, 'Deleted Selected', self.delete_command, 'Main Menu', lambda: controller.show_frame(MainMenu), self)

    def update_command(self):
        backend.update_events(selected_tuple[0], self.activity_id_text.get(), self.competitor_id_text.get(), self.score_id_text.get(), self.date_text.get(), self.event_type_text.get())

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
        for row in backend.activity_search(self.activity_id_text.get(), self.activity_description_text.get()):
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

        lblTitle = ttk.Label(self, text="Admin").grid(row=0, column=0)

        layout_frames(self)

        # Title header

        ttk.Label(self.header_frame, text='Administration', font=('monsterrat', 22, 'bold'), foreground='#6225da').grid(row=0, column=1, sticky='W')

        create_buttons('Delete Tables', self.delete_tables, 'Copy Database', self.copy_database, 'Delete Database Copy', self.delete_db_copy, 'Main Menu', lambda: controller.show_frame(MainMenu), self)

    def backup_database(self):
        backend.copy_db(self)

    def delete_database(self):
        backend.delete_database(self)

    def delete_tables(self):
        backend.drop_tables(self)

    def copy_database(self):
        backend.copy_db()

    def delete_db_copy(self):
        backend.delete_copy_db()

root = App()
root.mainloop()
