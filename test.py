import millenniumdb_driver as mdb

with mdb.driver("http://localhost:1234") as driver:
    with driver.session() as session:
        cat = session.catalog()
        print(cat.metadata)
