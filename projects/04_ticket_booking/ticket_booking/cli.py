"""Interactive menu for the cinema: `ticket-booking`."""

from collections.abc import Callable

from ticket_booking.models import BookingError, Cinema, Seat, demo_cinema


def parse_seats(text: str) -> list[Seat]:
    """Turn "1,2 3,4" into [(1, 2), (3, 4)]."""
    seats: list[Seat] = []
    for chunk in text.split():
        row, col = chunk.split(",")
        seats.append((int(row), int(col)))
    return seats


def run(
    cinema: Cinema, ask: Callable[[str], str] = input, say: Callable[[str], None] = print
) -> None:
    while True:
        say("\n1) View shows  2) Book seats  3) View seat map  4) Exit")
        choice = ask("Choose: ").strip()
        try:
            if choice == "1":
                for hall, show in cinema.shows():
                    say(
                        f"#{show.id} {show.movie} @ {show.time} "
                        f"(hall {hall.number}, {show.available()} free)"
                    )
            elif choice == "2":
                show = cinema.find_show(int(ask("Show id: ")))
                show.book(parse_seats(ask("Seats as row,col separated by spaces: ")))
                say("Booked!")
            elif choice == "3":
                say(cinema.find_show(int(ask("Show id: "))).seat_map())
            elif choice == "4":
                return
            else:
                say("Please choose 1-4.")
        # ValueError covers bad numbers typed by the user.
        except (BookingError, ValueError) as err:
            say(f"Error: {err}")


def main() -> int:
    try:
        run(demo_cinema())
    except (EOFError, KeyboardInterrupt):
        # Ctrl-D / Ctrl-C: leave cleanly instead of showing a traceback.
        print("\nGoodbye!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
