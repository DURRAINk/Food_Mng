import pandas as pd
from sqlalchemy import create_engine, text

claims= pd.read_csv("datasets/claims_data.csv")
food_listings = pd.read_csv("datasets/food_listings_data.csv")
providers = pd.read_csv("datasets/providers_data.csv")
receivers = pd.read_csv("datasets/receivers_data.csv")

engine = create_engine("sqlite:///food_management.db")
print(engine.url)


# SEARCH OPERATIONS-----------------------------------------------------------
def get_distinct_values():
    prov_names=list(pd.read_sql("select DISTINCT(Name) from providers", engine)['Name'])
    locations=list(pd.read_sql("select DISTINCT(Location) from food_listings", engine)['Location'])
    food_types=list(pd.read_sql("select DISTINCT(Food_Type) from food_listings", engine)['Food_Type'])
    return prov_names, locations, food_types
#Search Function
def search_food(opts):
    query = """
    SELECT pd.Name as Provider_Name, fl.Location, fl.Food_Type
    FROM providers pd
    JOIN food_listings fl ON pd.Provider_ID = fl.Provider_ID
    WHERE fl.Location = {} AND pd.Name = {} AND fl.Food_Type = {}
    """.format(opts['location'], opts['provider'], opts['food_type'])
    return pd.read_sql(query, engine)#, params=(opts['location'], opts['provider'], opts['food_type']))

# CRUD OPERATIONS-------------------------------------------------------------
tables = {"Claims Data":"claims","Food Listings Data":"food_listings","Providers Data":"providers","Receivers Data":"receivers"}

# to retrieve table from the database
def get_table_data(table_name):
    if table_name in tables:
        query = f"SELECT * FROM {tables[table_name]}"
        return pd.read_sql(query, engine)
    else:
        raise ValueError("Invalid table name provided.")
    

# to create query for updating records
def update_table(table_name,update_dict,lst,id):

    query =f"update {table_name} set "
    for col in update_dict:
        query += f"{col} = '{update_dict[col]}', "
    query = query.removesuffix(', ')+ f" where {lst[0]} = {id} "
    select = f"select * from {table_name} where {lst[0]} = {id};"
    with engine.begin() as conn:
        conn.execute(text(query))
    data = pd.read_sql(select, engine)
    return data

# to create query for inserting records
def insert_table(table_name,insert_dict):
    columns = ', '.join(insert_dict.keys())
    values = ', '.join([f"'{v}'" for v in insert_dict.values()])
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    with engine.begin() as conn:
        conn.execute(text(query))
    return pd.read_sql(f"SELECT * FROM {table_name} WHERE {list(insert_dict.keys())[0]} = '{list(insert_dict.values())[0]}'", engine)


# to create query for deleting records
def delete_record(table_name, id, lst):
    query = f"DELETE FROM {table_name} WHERE {lst[0]} = {id}"
    with engine.begin() as conn:
        conn.execute(text(query))
    

# Analysis Queries-------------------------------------------------------------
prov_city=list(pd.read_sql("select DISTINCT(City) from providers", engine)['City'])
sql_queries = ["select City, count(Name) as Provider_Count from providers group by City", "select City, count(Name) as Receiver_Count from receivers group by City",
           "select Type,count(Name)as Total from providers group by Type order by Total desc;",
            "SELECT Name, Contact FROM providers WHERE City = '{}';","select Name, count(Receiver_ID) as Total from (select rc.Name , cl.Receiver_ID from receivers rc join claims cl on rc.Receiver_ID = cl.Receiver_ID) as tables group by Name order by Total desc;",
            "select sum(Quantity) from food_listings;", "select City , sum(Quantity) as Total from (select pd.City, fl.Quantity from providers pd join food_listings fl on pd.Provider_ID = fl.Provider_ID) as tables group by City order by Total desc Limit 1;",
            "select Food_Type, count(Meal_Type) as Count from food_listings group by Food_Type order by Count desc;","select Food_Name, count(Claim_ID) as Total_Claims from (select fl.Food_Name, cm.Claim_ID from food_listings fl join claims cm on fl.Food_ID = cm.Food_ID) as tables group by Food_Name order by Total_Claims desc;",
            "select Name, count(Status) as Highest_Claims from (select pd.Name, cm.Status from providers pd join food_listings fl on pd.Provider_ID =fl.Provider_ID join claims cm on fl.Food_ID = cm.Food_ID where cm.Status = 'Completed') as tables group by Name order by Highest_Claims desc Limit 1;",
            "select Status, cast(Count(Claim_ID) as float)*100 /(select count(*) from claims) as [Status%] from Claims group by Status;", "select rv.Name as Receiver_Name, avg(fl.Quantity) as Avg_Quantity from receivers rv join claims cm on rv.Receiver_ID = cm.Receiver_ID join food_listings fl on fl.Food_ID = cm.Food_ID group by rv.Name order by Avg_Quantity desc;",
            "select fl.Meal_Type, count(cm.Status) as Count from claims cm join food_listings fl on cm.Food_ID = fl.Food_ID group by fl.Meal_Type order by Count desc;", "select pd.Name , sum(fl.Quantity) as Total_Qunatity from providers pd join food_listings fl on pd.Provider_ID = fl.Provider_ID group by pd.Name order by Total_Qunatity desc;",
            "select fl.Food_ID, fl.Food_Name, cm.Timestamp as Claim_Date, fl.Expiry_Date from claims cm join food_listings fl on cm.Food_ID = fl.Food_ID","select rc.Type as Receiver_Type , sum(fl.Quantity) as Total_Quantity from receivers rc join claims cm on rc.Receiver_ID = cm.Receiver_ID join food_listings as fl on cm.Food_ID = fl.Food_ID group by rc.Type order by Total_Quantity desc;"]

queries=["1. How many food providers and receivers are there in each city?",
    "2. Which type of food provider (restaurant, grocery store, etc.) contributes the most food?",
    "3. What is the contact information of food providers in a specific city?", "4. Which receivers have claimed the most food?",
    "5.  What is the total quantity of food available from all providers?","6. Which city has the highest number of food listings?",
    "7. What are the most commonly available food types?","8. How many food claims have been made for each food item?", 
    "9. Which provider has had the highest number of successful food claims?","10. What percentage of food claims are completed vs. pending vs. canceled?",
    "11. What is the average quantity of food claimed per receiver?","12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?",
    "13. What is the total quantity of food donated by each provider?","14. Claim date and expiry date of each food item",
    "15. Which type of Receiver has received the highest quantity of food?"]

# Contact Providers and Receivers-------------------------------------------------------------
def contact_providers():
    query = "SELECT Name, Contact FROM providers; "
    result = pd.read_sql(query, engine)
    return result

def contact_receivers():
    query = "SELECT Name, Contact FROM receivers; "
    result = pd.read_sql(query, engine)
    return result

print(engine.url)

