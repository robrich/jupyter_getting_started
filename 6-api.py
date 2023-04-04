import pandas as pd
from sqlalchemy import create_engine, text
from matplotlib import pyplot as plt
from fastapi import FastAPI
from io import BytesIO
from starlette.responses import StreamingResponse


pg_host = 'localhost'
pg_port = 5432
pg_user = 'postgres'
pg_pass = 'postgres'
pg_db = 'pgdb'

# TODO: read this on each request?
pg_engine = create_engine(f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
pg_conn = pg_engine.connect()
data = pd.read_sql_query(sql=text('select * from gapminder'), con=pg_conn)
pg_conn.close()

latest = data.year.max()
earliest = data.year.min()
years = data.year.unique()
print('years:', years)

app = FastAPI()

@app.get("/")
async def root():
    return {"urls": ["/docs", "/years", "/life-expectancy", "/population", "/gdp-per-capita"]}

@app.get("/years")
async def get_years():
    return years.tolist()

@app.get("/life-expectancy/{year}")
async def get_population(year: int = latest):

    year = valid_year(year)

    sel_year = data[data.year == year]
    continent = sel_year.groupby('continent')

    plt.clf()
    continent.mean().lifeExp.plot(title=f'Life Expectancy in {year}')

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.get("/population/{year}")
async def get_population(year: int = latest):

    year = valid_year(year)

    sel_year = data[data.year == year]
    continent = sel_year.groupby('continent')

    plt.clf()
    continent.pop.sum().plot(title=f'Population in {year}', kind='pie')

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.get("/gdp/{year}")
async def get_population(year: int = latest):

    year = valid_year(year)

    sel_year = data[data.year == year]
    continent = sel_year.groupby('continent')

    plt.clf()
    continent.gdpPercap.sum().plot(title=f'GDP per Capita in {year}')

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

def valid_year(year):

    if (year > latest):
        year = latest
    if (year < earliest):
        year = earliest
    if (year not in years):
        year = latest

    return year

print('Open http://localhost:8000/docs to see swagger page.')

# start app:
# python -m uvicorn 6-api:app --reload
