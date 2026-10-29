# Python OOP CLI Projects

![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue)
![Django 6](https://img.shields.io/badge/django-6.x-092e20)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

16 projects: 15 laddered command-line (CLI) projects for learning object-oriented (and functional) Python, from a first class to layered, tested applications, plus a Django + Django REST Framework (DRF) capstone. Each project has heavily commented source, tests and a list of exercises. The `docs/` folder has a concept guide for each topic, advanced Python guides, a full [Django & DRF track](docs/django/README.md) and interview Q&A.

## Website
Read everything as a searchable site: **[junaaid96.github.io/python-oop-cli-projects](https://junaaid96.github.io/python-oop-cli-projects/)** (guides, the Django & DRF track and every project with its source). It is built from this repo's Markdown by [`website/`](website/README.md) and deployed on each push to `main`.

## Table of contents
- [Website](#website)
- [Quick start](#quick-start)
- [Projects](#projects)
- [Concept guides](#concept-guides)
  - [Core OOP guides (01–18)](#core-oop-guides-0118)
  - [Advanced Python (19–24)](#advanced-python-1924)
  - [Django & DRF track (D01–D15)](#django--drf-track-d01d15)
- [Repository layout](#repository-layout)
- [Development](#development)
- [History](#history)
- [License](#license)

## Quick start
Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/junaaid96/python-oop-cli-projects.git
cd python-oop-cli-projects
uv sync                 # creates .venv with the projects and dev tools
uv run banking          # run any project by its command name
uv run pytest           # run all tests
```

## Projects
| # | Project | Level | Command | Key concepts |
|---|---|---|---|---|
| 01 | [Contact Book](projects/01_contact_book) | ⭐ Beginner | `contact-book` | classes, dataclasses, JSON storage |
| 02 | [Quiz Game](projects/02_quiz_game) | ⭐ Beginner | `quiz-game` | objects working together, scoring, `random` |
| 03 | [Todo Manager](projects/03_todo_manager) | ⭐ Beginner | `todo` | enums, repository, `argparse` |
| 04 | [Ticket Booking](projects/04_ticket_booking) | ⭐⭐ Beginner+ | `ticket-booking` | encapsulation, custom exceptions |
| 05 | [File Organizer](projects/05_file_organizer) | ⭐⭐ Beginner+ | `file-organizer` | functional style, `pathlib`, dry run |
| 06 | [Banking System + ATM](projects/06_banking_system) | ⭐⭐ Intermediate | `banking` | inheritance, ABC, `Decimal`, auth |
| 07 | [Expense Tracker](projects/07_expense_tracker) | ⭐⭐ Intermediate | `expense-tracker` | SQLite, reports, CSV |
| 08 | [Library Management](projects/08_library_management) | ⭐⭐ Intermediate | `library` | polymorphism, Protocol, dates |
| 09 | [Parking Lot](projects/09_parking_lot) | ⭐⭐ Intermediate | `parking-lot` | Strategy pattern, `IntEnum` |
| 10 | [Log Analyzer](projects/10_log_analyzer) | ⭐⭐ Intermediate | `log-analyzer` | generator pipelines, regex |
| 11 | [Ride Sharing](projects/11_ride_sharing) | ⭐⭐⭐ Advanced | `ride-sharing` | state machine, service layer |
| 12 | [Inventory & POS](projects/12_inventory_pos) | ⭐⭐⭐ Advanced | `inventory-pos` | Observer, composable discounts |
| 13 | [Hotel Reservation](projects/13_hotel_reservation) | ⭐⭐⭐ Advanced | `hotel` | layered architecture, repository |
| 14 | [URL Shortener](projects/14_url_shortener) | ⭐⭐⭐ Advanced | `url-shortener` | Protocol, dependency inversion |
| 15 | [Text Adventure](projects/15_text_adventure) | ⭐⭐⭐ Advanced | `text-adventure` | Command pattern, save/load |
| 16 | [FreelanceHub (Django + DRF)](projects/16_django_freelance_hub) | ⭐⭐⭐⭐ Capstone | `manage.py runserver` | ORM, N+1, CBV/FBV, forms, admin, REST API, permissions, pytest-django |

Each project folder has a README with what you'll learn, how to run it, and **exercises** to extend it.

## Concept guides
Start with the [learning path](docs/00_learning_path.md).

### Core OOP guides (01–18)

1. [Classes and objects](docs/01_classes_and_objects.md)
2. [Encapsulation](docs/02_encapsulation.md)
3. [Inheritance](docs/03_inheritance.md)
4. [Polymorphism](docs/04_polymorphism.md)
5. [Abstraction: ABC vs Protocol](docs/05_abstraction.md)
6. [Composition vs inheritance](docs/06_composition_vs_inheritance.md)
7. [Dataclasses, enums and type hints](docs/07_dataclasses_and_typing.md)
8. [Exceptions](docs/08_exceptions.md)
9. [Files, paths and JSON](docs/09_files_and_json.md)
10. [SQLite](docs/10_sqlite.md)
11. [Testing with pytest](docs/11_testing_with_pytest.md)
12. [CLI design](docs/12_cli_design.md)
13. [Packaging and tooling](docs/13_packaging_and_tooling.md)
14. [SOLID principles](docs/14_solid_principles.md)
15. [Design patterns](docs/15_design_patterns.md)
16. [Clean code](docs/16_clean_code.md)
17. [Functional programming](docs/17_functional_programming.md)
18. [OOP vs functional: when to use which](docs/18_oop_vs_functional.md)

### Advanced Python (19–24)

19. [Iterators and generators](docs/19_iterators_and_generators.md)
20. [Advanced typing](docs/20_advanced_typing.md)
21. [Concurrency and asyncio](docs/21_concurrency_and_asyncio.md)
22. [Virtual environments and packaging](docs/22_virtual_envs_and_packaging.md)
23. [Decorators and context managers](docs/23_decorators_and_context_managers.md)
24. [Python interview Q&A](docs/24_python_interview_qa.md)

### Django & DRF track (D01–D15)

Used by the [16 FreelanceHub](projects/16_django_freelance_hub) capstone. See the [track overview](docs/django/README.md) for what each guide covers and the suggested order.

| # | Guide |
|---|---|
| D01 | [Project structure](docs/django/01_project_structure.md) |
| D02 | [Models & ORM](docs/django/02_models_and_orm.md) |
| D03 | [Migrations](docs/django/03_migrations.md) |
| D04 | [Views](docs/django/04_views.md) |
| D05 | [Templates](docs/django/05_templates.md) |
| D06 | [Forms](docs/django/06_forms.md) |
| D07 | [Auth & permissions](docs/django/07_auth_and_permissions.md) |
| D08 | [Admin](docs/django/08_admin.md) |
| D09 | [Django REST Framework](docs/django/09_drf.md) |
| D10 | [Settings & config](docs/django/10_settings_and_config.md) |
| D11 | [Caching & Celery](docs/django/11_caching_and_celery.md) |
| D12 | [Security checklist](docs/django/12_security_checklist.md) |
| D13 | [Testing with pytest-django](docs/django/13_testing.md) |
| D14 | [Deployment](docs/django/14_deployment.md) |
| D15 | [Interview Q&A](docs/django/15_interview_qa.md) |

## Repository layout
```
projects/NN_name/
├── package/        # source (cli.py + domain modules)
├── tests/          # pytest suite
└── README.md       # concepts, run command, exercises
docs/               # concept guides (docs/django/ = Django & DRF track)
legacy/             # original scripts, kept with their git history
```

## Development
```bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run mypy                  # strict type check
uv run pytest                # tests
```
Run all four before every commit.

## History
This repo merges three earlier practice repos, with their full git history kept under `legacy/`:
- `ride_sharing` → rewritten as [11 Ride Sharing](projects/11_ride_sharing)
- `banking_system` → rewritten as [06 Banking System](projects/06_banking_system)
- `ticket-booking-system` → rewritten as [04 Ticket Booking](projects/04_ticket_booking)

## License
[MIT](LICENSE) © 2026 Md. Junaidul Islam
