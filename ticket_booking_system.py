class Star_Cinema:
  hall_list = []

  def entry_hall(self, hall):
    self.hall_list.append(hall)

star_cinema = Star_Cinema()
class Hall(Star_Cinema):

  def __init__(self, rows, cols, hall_no):
    self._seats = [[0 for i in range(cols)] for j in range(rows)]
    self._show_list = []
    self._rows = rows
    self._cols = cols
    self._hall_no = hall_no
    super().entry_hall(self)

  def entry_show(self, id, movie_name, time):
    show = (id, movie_name, time)
    self._show_list.append(show)

  def book_seats(self, show_id, seat_list):
    for show in self._show_list:
      if show[0] == show_id:
        seats = self._seats
        for row, col in seat_list:
          if 1 <= row <= self._rows and 1 <= col <= self._cols:
            if seats[row - 1][col - 1] == 0:
              seats[row - 1][col - 1] = 1
              print(f"Seat booked at ({row},{col}).")
            else:
              print(f"Seat ({row},{col}) is already booked!")
          else:
            print("Invalid seat input!")
        break
    else:
      print("Show is not found!")

  def view_show_list(self):
    print("List of Shows:")
    for show in self._show_list:
      print(f"ID: {show[0]}, Movie: {show[1]}, Time: {show[2]}")

  def view_available_seats(self, show_id):
    for show in self._show_list:
      if show[0] == show_id:
        seats = self._seats
        print(f"Available seats for show ID {show_id}: ")
        for row in range(self._rows):
          for col in range(self._cols):
            if seats[row][col] == 0:
              print("O", end=" ")
            else:
              print("1", end=" ")
          print()
        break
    else:
      print("Show is not found!")

hall_101 = Hall(10, 10, 101)
hall_101.entry_show(111, "3 Idiots", "21-10-23 3PM")
hall_101.entry_show(333, "Chhichhore", "22-10-23 6PM")

while True:
  print("1. View all shows")
  print("2. Book ticket")
  print("3. View available seats")
  print("4. Exit")

  option = input("Enter Option: ")

  if option == "1":
    for hall in star_cinema.hall_list:
      hall.view_show_list()

  elif option == "2":
    show_id = int(input("Show ID: "))
    num_seats = int(input("Number of seats to book: "))
    seat_list = []
    for i in range(num_seats):
      row = int(input(f"Enter row for seat {i+1}: "))
      col = int(input(f"Enter column for seat {i+1}: "))
      seat_list.append((row, col))
    for hall in star_cinema.hall_list:
      hall.book_seats(show_id, seat_list)

  elif option == "3":
    show_id = int(input("Enter the show ID: "))
    for hall in star_cinema.hall_list:
      hall.view_available_seats(show_id)

  elif option == "4":
    break
  
  else:
    print("Please select a valid option.")
