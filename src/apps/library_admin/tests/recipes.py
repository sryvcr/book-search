from model_bakery.recipe import Recipe, related


author_alex_xu = Recipe(
    "library_admin.Author",
    name="Alex Xu",
)

author_sahn_lam = Recipe(
    "library_admin.Author",
    name="Sahn Lam",
)

category_computer = Recipe(
    "library_admin.Category",
    name="Computer",
)

category_web_development = Recipe(
    "library_admin.Category",
    name="Web Development",
)


book_system_design_interview = Recipe(
    "library_admin.Book",
    title="System Design Interview",
    subtitle="An Insider's Guide, Second Edition",
    publication_date="2020-02-12",
    editor="ByteByteGo",
    description="System Design Interview book description",
    image="http://books.google.com.co/books?id=TZWmzQEACAAJ&dq=alex+xu&hl=&cd=2&source=gbs_api",
    author=related(
        author_alex_xu,
        author_sahn_lam,
    ),
    category=related(
        category_computer,
        category_web_development,
    ),
)
