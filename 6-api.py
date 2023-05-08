import pandas as pd
from sqlalchemy import create_engine, text
from matplotlib import pyplot as plt
from fastapi import FastAPI
from io import BytesIO
from starlette.responses import StreamingResponse

# TODO: get from env vars
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
countries = data.country.unique()

app = FastAPI()

@app.get("/")
async def root():
    return {"urls": ["/docs", "/years", "/life-expectancy/{year}", "/population/{year}", "/gdp-per-capita/{year}", "/countries", "/country/{country_name}"]}

@app.get("/years")
async def get_years():
    return years.tolist()

@app.get("/life-expectancy/{year}")
async def get_population(year: int = latest):

    year = valid_year(year)

    sel_year = data[data.year == year]
    continent = sel_year.groupby('continent')

    plt.clf()
    continent.mean().lifeExp.plot(title=f'Life Expectancy in {year}', kind='bar')

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
    continent.gdpPercap.sum().plot(title=f'GDP per Capita in {year}', kind='bar')

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

@app.get("/countries")
async def get_countries():
    return countries.tolist()

@app.get("/country/{country_name}")
async def get_country(country_name: str = 'United States'):

    if (valid_country(country_name) == False):
        return {"error": "invalid country"}

    country = data[data.country == country_name]

    plt.clf()

    fig, ax1 = plt.subplots(1,1)

    ax1.plot(country['year'], country['lifeExp'], 'red', linestyle='-', label='life expectancy')
    ax1.set_xlabel('year')
    ax1.set_ylabel('life expectancy', color='r')
    ax1.tick_params('y', colors='r')

    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.2)) # move the axis right a bit
    ax2.plot(country['year'], country['pop'], 'blue', linestyle=':', label='population')
    ax2.set_ylabel('population (Mil)', color='blue')
    ax2.tick_params('y', colors='blue')

    ax3 = ax1.twinx()
    ax3.plot(country['year'], country['gdpPercap'], 'black', linestyle='--', label='gdp per capita')
    ax3.set_ylabel('gdp per capita', color='black')
    ax3.tick_params('y', colors='black')

    fig.tight_layout()

    plt.title(f'{country_name}, {country.continent.unique()[0]}')

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

def valid_country(country):
    return (country in countries)


print('Open http://localhost:8000/docs to see swagger page.')

# start app:
# uvicorn 6-api:app --reload
