from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.books.models import Book, Review

User = get_user_model()

SEED_PASSWORD = "Bookstore123!"

BOOKS = [
    {
        "isbn": "9780132350884",
        "title": "Clean Code",
        "author_name": "Robert C. Martin",
        "description": "A handbook of agile software craftsmanship: names, functions, and how to keep code readable.",
    },
    {
        "isbn": "9780201633610",
        "title": "Design Patterns",
        "author_name": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "description": "Classic catalog of reusable object-oriented design patterns.",
    },
    {
        "isbn": "9780134685991",
        "title": "Effective Java",
        "author_name": "Joshua Bloch",
        "description": "Best practices for writing clear, correct, and efficient Java.",
    },
    {
        "isbn": "9780135957059",
        "title": "The Pragmatic Programmer",
        "author_name": "David Thomas, Andrew Hunt",
        "description": "Timeless tips for taking responsibility for your craft.",
    },
    {
        "isbn": "9780596007126",
        "title": "Head First Design Patterns",
        "author_name": "Eric Freeman, Elisabeth Robson",
        "description": "Design patterns explained with a visual, example-driven style.",
    },
    {
        "isbn": "9780134494166",
        "title": "Clean Architecture",
        "author_name": "Robert C. Martin",
        "description": "How to structure systems so business rules stay independent of frameworks.",
    },
    {
        "isbn": "9780321125217",
        "title": "Domain-Driven Design",
        "author_name": "Eric Evans",
        "description": "Tackling complexity in the heart of software through a shared model.",
    },
    {
        "isbn": "9780131103627",
        "title": "The C Programming Language",
        "author_name": "Brian W. Kernighan, Dennis M. Ritchie",
        "description": "The concise reference that defined C for a generation of programmers.",
    },
    {
        "isbn": "9780262033848",
        "title": "Introduction to Algorithms",
        "author_name": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "description": "A comprehensive textbook of algorithms and data structures.",
    },
    {
        "isbn": "9780132350885",
        "title": "Refactoring",
        "author_name": "Martin Fowler",
        "description": "Improving the design of existing code in small, safe steps.",
    },
    {
        "isbn": "9780201616224",
        "title": "The Mythical Man-Month",
        "author_name": "Frederick P. Brooks Jr.",
        "description": "Essays on software engineering and why adding people can delay a late project.",
    },
    {
        "isbn": "9780596517748",
        "title": "JavaScript: The Good Parts",
        "author_name": "Douglas Crockford",
        "description": "A focused tour of the reliable core of JavaScript.",
    },
    {
        "isbn": "9781491950357",
        "title": "Building Microservices",
        "author_name": "Sam Newman",
        "description": "Designing fine-grained systems with independent deployable services.",
    },
    {
        "isbn": "9781449373320",
        "title": "Designing Data-Intensive Applications",
        "author_name": "Martin Kleppmann",
        "description": "Reliability, scalability, and maintainability of modern data systems.",
    },
    {
        "isbn": "9780134092669",
        "title": "Computer Networking: A Top-Down Approach",
        "author_name": "James Kurose, Keith Ross",
        "description": "Networks explained from applications down to the physical layer.",
    },
    {
        "isbn": "9780131101630",
        "title": "The Art of Computer Programming, Volume 1",
        "author_name": "Donald E. Knuth",
        "description": "Fundamental algorithms presented with mathematical rigor.",
    },
    {
        "isbn": "9780596009205",
        "title": "Head First Java",
        "author_name": "Kathy Sierra, Bert Bates",
        "description": "An approachable introduction to Java and object-oriented thinking.",
    },
    {
        "isbn": "9781617294136",
        "title": "Spring in Action",
        "author_name": "Craig Walls",
        "description": "Building applications with the Spring Framework.",
    },
    {
        "isbn": "9781484240779",
        "title": "Two Scoops of Django",
        "author_name": "Daniel Roy Greenfeld, Audrey Roy Greenfeld",
        "description": "Opinions and patterns for Django that stay maintainable.",
    },
    {
        "isbn": "9781593279288",
        "title": "Python Crash Course",
        "author_name": "Eric Matthes",
        "description": "A hands-on introduction to Python through projects.",
    },
    {
        "isbn": "9781492056355",
        "title": "Fluent Python",
        "author_name": "Luciano Ramalho",
        "description": "Idiomatic Python: data model, functions, objects, and concurrency.",
    },
    {
        "isbn": "9780134757599",
        "title": "Refactoring UI",
        "author_name": "Adam Wathan, Steve Schoger",
        "description": "Practical visual design for developers who ship interfaces.",
    },
    {
        "isbn": "9780321349606",
        "title": "Java Concurrency in Practice",
        "author_name": "Brian Goetz",
        "description": "How to write correct concurrent programs on the JVM.",
    },
    {
        "isbn": "9780137081073",
        "title": "The Clean Coder",
        "author_name": "Robert C. Martin",
        "description": "Professionalism, saying no, and the discipline of software work.",
    },
    {
        "isbn": "9780596007127",
        "title": "Don't Make Me Think",
        "author_name": "Steve Krug",
        "description": "Common-sense usability for web and application interfaces.",
    },
    {
        "isbn": "9780465026562",
        "title": "The Design of Everyday Things",
        "author_name": "Don Norman",
        "description": "Why some products feel obvious and others fight their users.",
    },
    {
        "isbn": "9780062316097",
        "title": "Sapiens",
        "author_name": "Yuval Noah Harari",
        "description": "A brief history of humankind, from foraging bands to global networks.",
    },
    {
        "isbn": "9780553380163",
        "title": "A Brief History of Time",
        "author_name": "Stephen Hawking",
        "description": "Black holes, the Big Bang, and the shape of the universe for general readers.",
    },
    {
        "isbn": "9780143124177",
        "title": "Thinking, Fast and Slow",
        "author_name": "Daniel Kahneman",
        "description": "The two systems that drive how we think and how we judge.",
    },
    {
        "isbn": "9780385474542",
        "title": "Zen and the Art of Motorcycle Maintenance",
        "author_name": "Robert M. Pirsig",
        "description": "A journey that asks what quality means in work and in life.",
    },
]

USERS = [
    ("admin@bookstore.local", "Admin", "User", True),
    ("maya@bookstore.local", "Maya", "Hassan", False),
    ("omar@bookstore.local", "Omar", "Farouk", False),
    ("lina@bookstore.local", "Lina", "Mostafa", False),
    ("karim@bookstore.local", "Karim", "Nabil", False),
    ("sara@bookstore.local", "Sara", "Adel", False),
    ("youssef@bookstore.local", "Youssef", "Samir", False),
    ("noura@bookstore.local", "Noura", "Hany", False),
    ("tamer@bookstore.local", "Tamer", "Fouad", False),
    ("dina@bookstore.local", "Dina", "Khaled", False),
]

REVIEW_COMMENTS = [
    (5, "Clear, practical, and still useful years after the first read."),
    (4, "Strong ideas. A few chapters feel dated, but the core holds up."),
    (5, "I keep coming back to this whenever a design starts to sprawl."),
    (3, "Good material, though it takes patience to get through the denser parts."),
    (4, "Helped me explain the same topic to teammates in simpler words."),
    (2, "Not what I expected. Fine as a reference, slow as a cover-to-cover read."),
    (5, "One of the books I actually finished and recommended the same week."),
    (4, "Solid examples. I wished it had more on testing."),
    (3, "Interesting, but I needed another source to apply it at work."),
    (5, "Changed how I name things and split functions."),
]


def _content(title, author_name, description):
    return (
        f"{title}\n"
        f"by {author_name}\n\n"
        f"{description}\n\n"
        "Chapter 1\n\n"
        "The opening chapter sets the vocabulary for the rest of the book. "
        "Instead of rushing into tools, it spends time on the problem the reader "
        "actually has: unclear code, unclear intent, and systems that become "
        "expensive to change. Short examples show the difference between code "
        "that merely runs and code that a teammate can trust.\n\n"
        "Chapter 2\n\n"
        "Here the author slows down. Each idea is shown twice: once in a messy "
        "form that looks familiar, and once after a careful rewrite. The point is "
        "not cleverness. The point is that small, boring decisions compound. "
        "Names, boundaries, and tests are treated as part of the same craft.\n\n"
        "Chapter 3\n\n"
        "The later pages connect the early lessons to larger design. You see how "
        "a module that looked harmless on day one becomes a bottleneck, and how "
        "a slightly stricter structure would have left more room to grow. The "
        "book ends by asking the reader to practice on real work, not on toys."
    )


class Command(BaseCommand):
    help = "Load a sizable catalog of books, demo users, and reviews."

    def handle(self, *args, **options):
        users = []
        for email, first_name, last_name, is_admin in USERS:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_staff": is_admin,
                    "is_superuser": is_admin,
                },
            )
            if created:
                user.set_password(SEED_PASSWORD)
                user.save(update_fields=["password"])
            users.append(user)

        books = []
        for item in BOOKS:
            book, _ = Book.objects.update_or_create(
                isbn=item["isbn"],
                defaults={
                    "title": item["title"],
                    "author_name": item["author_name"],
                    "description": item["description"],
                    "content": _content(item["title"], item["author_name"], item["description"]),
                },
            )
            books.append(book)

        readers = [user for user in users if not user.is_superuser]
        review_count = 0
        for index, book in enumerate(books):
            for offset in range(3):
                user = readers[(index + offset) % len(readers)]
                rating, comment = REVIEW_COMMENTS[(index + offset) % len(REVIEW_COMMENTS)]
                _, created = Review.objects.get_or_create(
                    user=user,
                    book=book,
                    defaults={"rating": rating, "comment": comment},
                )
                if created:
                    review_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete: {len(books)} books, {len(users)} users, "
                f"{review_count} new reviews. Password for all seed users: {SEED_PASSWORD}"
            )
        )
