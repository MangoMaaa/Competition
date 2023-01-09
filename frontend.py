import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

import backend as backend


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
            frame.grid(row=0, column=0, sticky="nsew")
        print(self.frames)

        self.show_frame(MainMenu)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class MainMenu(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        lblMainMenu = ttk.Label(self, text="Main Menu")
        lblMainMenu.grid(row=0, column=0, sticky="w")

        # self.neco_arc = ImageTk.PhotoImage(file='Neco-Arc_Remake (1).png')
        # tk.Label(self.header_frame, image=self.neco_arc, anchor='w').grid(row=0, column=0, sticky='w')
        # img_neco_arc = Image.open('Neco-Arc_Remake (1).png')
        # resizedImage = img_neco_arc.resize((332, 210), Image.Resampling.LANCZOS)
        # img_neco_arc = ImageTk.PhotoImage(resizedImage)
        # my_image = ttk.Label(self, image=img_neco_arc)
        # my_image.image = img_neco_arc
        # my_image.grid(row=2, rowspan=6, column=0)

        btnCompTeam = ttk.Button(self, text='Competitor(s)', width=15, command=lambda: controller.show_frame(Competitors))
        btnCompTeam.grid(row=1, column=1, padx=10, pady=15)

        btnEvents = ttk.Button(self, text='Events', width=15, command=lambda: controller.show_frame(Events))
        btnEvents.grid(row=2, column=1, padx=10, pady=15)

        btnLeaderBoards = ttk.Button(self, text='LeaderBoards', width=15, command=lambda: controller.show_frame(Leaderboards))
        btnLeaderBoards.grid(row=3, column=1, padx=10, pady=15)

        btnActivities = ttk.Button(self, text='Activities', width=15, command=lambda: controller.show_frame(Activities))
        btnActivities.grid(row=4, column=1, padx=10, pady=15)

        btnAdmin = ttk.Button(self, text='Admin', width=15, command=lambda: controller.show_frame(Admin))
        btnAdmin.grid(row=5, column=1, padx=10, pady=15)

        btnExit = ttk.Button(self, text='Exit', width=15, command=lambda: controller.show_frame(exit()))
        btnExit.grid(row=6, column=1, padx=10, pady=15)

        # image
        placeholder = Image.open("Neco-Arc_Remake (1).png")
        resizedImage = placeholder.resize((332, 400), Image.Resampling.LANCZOS)
        placeholder = ImageTk.PhotoImage(resizedImage)
        placeholder_image = ttk.Label(self, image=placeholder)
        placeholder_image.image = placeholder
        placeholder_image.grid(row=7, column=5, sticky="ns")


class Competitors(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.Forename_text = tk.StringVar()
        self.Surname_text = tk.StringVar()
        self.Team_Name_text = tk.StringVar()
        self.Competitor_ID_text = tk.StringVar()
        self.Competitor_Type_ID_text = tk.StringVar()
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=0, column=0)

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

        text = ['Forename:', 'Surname:', 'Team Name:', 'Competitor ID:', 'Competitor Type ID:']
        for i in range(len(text)):
            ttk.Label(self.data_entry_frame, text=text[i]).grid(row=i, column=5, ipadx=1, ipady=5, padx=1, pady=10, sticky="e")

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
            button.grid(row=0, column=i + 1, padx=5, pady=10, sticky='n')

        '''
        ttk.Button(self.buttons_frame, text='View All', width=14, command=self.view_all_command).grid(row=0, column=1, padx=5, pady=10,sticky='n')
        ttk.Button(self.buttons_frame, text='Search', width=14, command=self.competitor_search_command).grid(row=0, column=2, padx=5, pady=10, sticky='n')
        ttk.Button(self.buttons_frame, text='Add', width=14, command=self.add_command).grid(row=0, column=3, padx=5, pady=10, sticky='n')
        ttk.Button(self.buttons_frame, text='Update Selected', width=14, command=self.update_command).grid(row=0, column=4, padx=6, pady=10, sticky='n')
        ttk.Button(self.buttons_frame, text='Delete Selected', width=14, command=self.delete_command).grid(row=0, column=5, padx=6, pady=10, sticky='n')
        ttk.Button(self.buttons_frame, text='Main Menu', width=14, command=lambda: controller.show_frame(MainMenu)).grid(row=0, column=6, padx=6, pady=10, sticky='n')
        '''

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

        ttk.Label(self.data_entry_frame, text="Event").grid(row=0, column=0, ipadx=5, ipady=5, padx=10, pady=10, sticky="w")
        ttk.Label(self.data_entry_frame, text="Competitor ID").grid(row=1, column=0, ipadx=5, ipady=5, padx=10, pady=10, sticky="w")
        ttk.Label(self.data_entry_frame, text="Activity ID").grid(row=2, column=0, ipadx=5, ipady=5, padx=10, pady=10, sticky="w")
        ttk.Label(self.data_entry_frame, text="Score").grid(row=3, column=0, ipadx=5, ipady=5, padx=10, pady=10, sticky="w")
        ttk.Label(self.data_entry_frame, text="Event ID").grid(row=4, column=0, ipadx=5, ipady=5, padx=10, pady=10, sticky="w")

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
            button.grid(row=0, column=i, padx=5, pady=5, sticky='n')


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
        self.lstResults.delete(0,'end')
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

        lblTitle = ttk.Label(self, text="Leaderboards")
        lblTitle.grid(row=0, column=0)


class Activities(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        lblTitle = ttk.Label(self, text="Activities")
        lblTitle.grid(row=0, column=0)


class Admin(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        lblTitle = ttk.Label(self, text="Admin")
        lblTitle.grid(row=0, column=0)


root = App()
root.mainloop()