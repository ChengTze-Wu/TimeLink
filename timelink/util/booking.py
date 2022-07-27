from datetime import date, time

class Booking():
    def __init__(self, open_time, close_time, not_available_time):
        self.__open_time = open_time
        self.__close_time = close_time
        self.__not_available_time = not_available_time
    
    def book(self, start_time, end_time):
        pass