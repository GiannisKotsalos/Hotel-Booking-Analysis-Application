import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

def read_dataset(file_name='hotel_booking.csv'):
    try:
        return pd.read_csv(file_name)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def Total_Nights_Spent(df):
    df['total_nights_spent'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    
    hotel_types = ['Resort Hotel', 'City Hotel']
    total_nights_list = []
    average_nights_list = []

    for hotel_type in hotel_types:
        df_hotel = df[df['hotel'] == hotel_type]

        total_nights = df_hotel['total_nights_spent'].sum()
        total_bookings = df_hotel.shape[0]
        average_nights_per_booking = total_nights / total_bookings

        total_nights_list.append(total_nights)
        average_nights_list.append(average_nights_per_booking)

    labels = ['Resort Hotel', 'City Hotel']
    total_nights_df = pd.DataFrame({
        'Hotel Type': labels,
        'Total Nights': total_nights_list,
        'Average Nights per Booking': average_nights_list
    })
    total_nights_df.to_csv('total_nights_spent.csv', index=False)

    x = range(len(labels))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.bar(x, total_nights_list, color='blue')
    ax1.set_title('Total Nights Spent')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_ylabel('Total Nights')

    ax2.bar(x, average_nights_list, color='orange')
    ax2.set_title('Average Nights per Booking')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.set_ylabel('Average Nights')

    plt.tight_layout()
    plt.show()

def Percentage_Of_Cancelation(df):
    total_bookings = df.shape[0]
    total_number_of_cancellation = df['is_canceled'].sum()
    percentage_of_cancellation = (total_number_of_cancellation / total_bookings) * 100

    cancellation_df = pd.DataFrame({
        'Status': ['Canceled', 'Not Canceled'],
        'Percentage': [percentage_of_cancellation, 100 - percentage_of_cancellation]
    })
    cancellation_df.to_csv('percentage_of_cancellation.csv', index=False)

    labels = ['Canceled', 'Not Canceled']
    sizes = [percentage_of_cancellation, 100 - percentage_of_cancellation]
    explode = (0.1, 0)
    plt.figure()
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Cancellation Rate')
    plt.show()

def Bookings_Per_Time(df):
    bookings_per_month = df['arrival_date_month'].value_counts().sort_index()

    seasons = {
        'Spring': ['March', 'April', 'May'],
        'Summer': ['June', 'July', 'August'],
        'Autumn': ['September', 'October', 'November'],
        'Winter': ['December', 'January', 'February']
    }

    df['season'] = df['arrival_date_month'].apply(lambda x: next((season for season, months in seasons.items() if x in months), 'Unknown'))
    
    bookings_per_season = df['season'].value_counts().sort_index()

    bookings_per_month_df = bookings_per_month.reset_index()
    bookings_per_month_df.columns = ['Month', 'Number of Bookings']
    bookings_per_month_df.to_csv('bookings_per_month.csv', index=False)

    bookings_per_season_df = bookings_per_season.reset_index()
    bookings_per_season_df.columns = ['Season', 'Number of Bookings']
    bookings_per_season_df.to_csv('bookings_per_season.csv', index=False)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    bookings_per_month.plot(kind='bar', ax=axs[0], color='skyblue')
    axs[0].set_title('Bookings per Month')
    axs[0].set_xlabel('Month')
    axs[0].set_ylabel('Number of Bookings')

    bookings_per_season.plot(kind='bar', ax=axs[1], color='lightgreen')
    axs[1].set_title('Bookings per Season')
    axs[1].set_xlabel('Season')
    axs[1].set_ylabel('Number of Bookings')
    plt.tight_layout()
    plt.show()

def Reservations_Per_RoomType(df):
    reservations_per_roomType = df['reserved_room_type'].value_counts()

    reservations_per_roomType_df = reservations_per_roomType.reset_index()
    reservations_per_roomType_df.columns = ['Room Type', 'Number of Reservations']
    reservations_per_roomType_df.to_csv('reservations_per_room_type.csv', index=False)

    plt.figure()
    reservations_per_roomType.plot(kind='bar', color='salmon')
    plt.title('Reservations per Room Type')
    plt.xlabel('Room Type')
    plt.ylabel('Number of Reservations')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def Types_Of_Reservations(df):
    family_bookings = df[(df['adults'] > 0) & ((df['children'] > 0) | (df['babies'] > 0))]
    couple_bookings = df[(df['adults'] == 2) & (df['children'] == 0) & (df['babies'] == 0)]
    solo_traveler_bookings = df[(df['adults'] == 1) & (df['children'] == 0) & (df['babies'] == 0)]

    num_families = len(family_bookings)
    num_couples = len(couple_bookings)
    num_solo_travelers = len(solo_traveler_bookings)

    types_of_reservations_df = pd.DataFrame({
        'Reservation Type': ['Families', 'Couples', 'Solo Travelers'],
        'Number of Reservations': [num_families, num_couples, num_solo_travelers]
    })
    types_of_reservations_df.to_csv('types_of_reservations.csv', index=False)

    labels = ['Families', 'Couples', 'Solo Travelers']
    sizes = [num_families, num_couples, num_solo_travelers]
    explode = (0.1, 0, 0)
    plt.figure()
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Types of Reservations')
    plt.show()

def Booking_Trends(df):
    booking_trends = df.groupby(['arrival_date_year', 'arrival_date_month']).size().reset_index(name='num_bookings')
    booking_trends['time'] = booking_trends['arrival_date_month'] + ' ' + booking_trends['arrival_date_year'].astype(str)

    booking_trends.to_csv('booking_trends.csv', index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(booking_trends['time'], booking_trends['num_bookings'], marker='o')
    plt.title('Booking Trends Over Time')
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Bookings')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def Cancellation_Trends(df):
    cancellation_trends = df[df['is_canceled'] == 1].groupby(['arrival_date_year', 'arrival_date_month']).size().reset_index(name='num_cancellations')
    cancellation_trends['time'] = cancellation_trends['arrival_date_month'] + ' ' + cancellation_trends['arrival_date_year'].astype(str)

    cancellation_trends.to_csv('cancellation_trends.csv', index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(cancellation_trends['time'], cancellation_trends['num_cancellations'], marker='o', color='red')
    plt.title('Cancellation Trends Over Time')
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Cancellations')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Hotel Booking Analysis'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()

        total_nights_btn = QPushButton('Total Nights Spent', self)
        total_nights_btn.clicked.connect(self.show_Total_Nights_Spent)
        layout.addWidget(total_nights_btn)

        percentage_of_cancellation_btn = QPushButton('Percentage Of Cancellation', self)
        percentage_of_cancellation_btn.clicked.connect(self.show_Percentage_Of_Cancelation)
        layout.addWidget(percentage_of_cancellation_btn)

        bookings_per_time_btn = QPushButton('Bookings Per Time', self)
        bookings_per_time_btn.clicked.connect(self.show_Bookings_Per_Time)
        layout.addWidget(bookings_per_time_btn)

        reservations_per_roomtype_btn = QPushButton('Reservations Per Room Type', self)
        reservations_per_roomtype_btn.clicked.connect(self.show_Reservations_Per_RoomType)
        layout.addWidget(reservations_per_roomtype_btn)

        types_of_reservations_btn = QPushButton('Types Of Reservations', self)
        types_of_reservations_btn.clicked.connect(self.show_Types_Of_Reservations)
        layout.addWidget(types_of_reservations_btn)

        booking_trends_btn = QPushButton('Booking Trends', self)
        booking_trends_btn.clicked.connect(self.show_Booking_Trends)
        layout.addWidget(booking_trends_btn)

        cancellation_trends_btn = QPushButton('Cancellation Trends', self)
        cancellation_trends_btn.clicked.connect(self.show_Cancellation_Trends)
        layout.addWidget(cancellation_trends_btn)

        self.setLayout(layout)
        self.show()

    def show_Total_Nights_Spent(self):
        df = read_dataset()
        if df is not None:
            Total_Nights_Spent(df)

    def show_Percentage_Of_Cancelation(self):
        df = read_dataset()
        if df is not None:
            Percentage_Of_Cancelation(df)

    def show_Bookings_Per_Time(self):
        df = read_dataset()
        if df is not None:
            Bookings_Per_Time(df)

    def show_Reservations_Per_RoomType(self):
        df = read_dataset()
        if df is not None:
            Reservations_Per_RoomType(df)

    def show_Types_Of_Reservations(self):
        df = read_dataset()
        if df is not None:
            Types_Of_Reservations(df)

    def show_Booking_Trends(self):
        df = read_dataset()
        if df is not None:
            Booking_Trends(df)

    def show_Cancellation_Trends(self):
        df = read_dataset()
        if df is not None:
            Cancellation_Trends(df)

def main():
    app = QApplication([])
    ex = App()
    app.exec_()

if __name__ == "__main__":
    main()
