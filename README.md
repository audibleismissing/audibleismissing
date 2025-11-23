mkdir audibleismissing-fastapi
cd audibleismissing-fastapi

uv init

uv add fastapi --extra standard
uv add audible
uv add requests
uv add sqlmodel
uv add toml
uv add jinja2

uv tool install ruff


mkdir -p {app, app/templates, app/static, app/routers, app/db_models}





## Docker operations
docker system prune -f


docker compose down
docker rm audibleismissing-fastapi-dev-1 
docker rmi audibleismissing-fastapi-dev:latest
docker compose -f dev-compose.yaml up --build



docker exec -it audibleismissing-fastapi-dev-1 sh



## Non docker operations
uv run fastapi dev main.py



https://fastapi.tiangolo.com/advanced/templates/?h=template#using-jinja2templates
https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter




max books returned by audible api is 50



/api/book/{title or bookAsin}
getBook -> Book

/api/books/all/
getAllBooks -> [Book]

/api/books/series/{seriesName}
getBooksInSeries -> [Book]

/api/books/author/{authorName}
getBooksByAuthor -> [Book]




/api/series/all/
getAllSeries -> [Series]


/api/series/{name or seriesAsin}
getSeries -> Series

/api/series/book/{title or bookAsin}
getSeriesByBook => [Series]




getAuthor -> Author
getAuthorByBook => [Author]


getNarrator -> Narrator
getNarratorByBook => [Narrator]


getGenre -> Genre
getGenreByBook => [Genre]







## Uses
https://getbootstrap.com
https://bootstrap-table.com
https://jquery.com