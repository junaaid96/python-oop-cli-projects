# Ticket Booking System: Star Cinema

Star Cinema is a Python program that simulates the management of cinema halls and movie shows. It includes two classes: Star_Cinema and Hall.

## Star_Cinema Class

The `Star_Cinema` class contains a class attribute named `hall_list`, which is initially an empty list. It provides a method to insert objects of the `Hall` class into its `hall_list`.

### Methods

#### 1. `entry_hall(hall)`

   - This method allows you to insert an object of the `Hall` class into the `hall_list` attribute.

## Hall Class

The `Hall` class represents an individual cinema hall. It has five instance attributes:

1. `seats`: A dictionary that stores seat information.
2. `show_list`: A list of tuples representing shows in the hall.
3. `rows`: The number of rows in the hall.
4. `cols`: The number of columns in the hall.
5. `hall_no`: A unique identifier for the hall.

### Methods

#### 1. `entry_show(id, movie_name, time)`

   - This method allows you to add a new show to the `show_list`. It creates a tuple with information about the show (ID, movie name, and time). Seats are allocated using a 2D list, with all seats initially set to "free" (means 0)

#### 2. `book_seats(id, seat_list)`

   - This method allows you to book seats for a specific show. It takes the show ID and a list of tuples, where each tuple contains the row and column of the seats to be booked. The method handles errors, such as invalid show IDs, attempts to book already booked seats, and invalid seat selections.

#### 3. `view_show_list()`

   - This method allows you to view a list of all shows currently running in the hall.

#### 4. `view_available_seats(id)`

   - This method takes a show ID as input and displays the available seats for that show. It also handles errors, such as incorrect show IDs.
