from sqlalchemy import create_engine, text, Table ,Column, Integer, String, MetaData, DATETIME, ForeignKey
import pandas as pd

claims_data= pd.read_csv("datasets/claims_data.csv")
food_listings_data = pd.read_csv("datasets/food_listings_data.csv")
providers_data = pd.read_csv("datasets/providers_data.csv")
receivers_data = pd.read_csv("datasets/receivers_data.csv")

engine = create_engine("sqlite:///food_management.db",echo=True)
metadata=MetaData()
metadata.drop_all(bind=engine)

receivers=Table("receivers",metadata,
      Column("Receiver_ID",Integer, primary_key=True,autoincrement=True),
      Column("Name", String(25)),
      Column("Type", String(15)),
      Column("City", String(20)),
      Column("Contact", String(25)))

providers=Table("providers",metadata,
      Column("Provider_ID", Integer, primary_key=True, autoincrement=True),
      Column("Name", String(25)),
      Column("Type", String(15)),
      Column("Address", String(100)),
      Column("City", String(20)),
      Column("Contact", String(25)))

food_listings=Table("food_listings",metadata,
      Column("Food_ID",Integer, primary_key=True,autoincrement=True),
      Column("Food_Name", String(10)),
      Column("Quantity", Integer),
      Column("Expiry_Date", DATETIME),
      Column("Provider_ID", Integer,ForeignKey("providers.Provider_ID")),
      Column("Provider_Type",String(20)),
      Column("Location", String(20)),
      Column("Food_Type", String(15)),
      Column("Meal_Type", String(15)))

claims=Table("claims",metadata,
      Column("Claim_ID",Integer,primary_key=True, autoincrement=True),
      Column("Food_ID", Integer,ForeignKey("food_listings.Food_ID")),
      Column("Receiver_ID",Integer,ForeignKey("receivers.Receiver_ID")),
      Column("Status",String(10)),
      Column("Timestamp",DATETIME))

metadata.create_all(engine)

claims_data.to_sql('claims', engine, index=False, if_exists='append')
food_listings_data.to_sql('food_listings', engine, index=False, if_exists='append')
providers_data.to_sql('providers', engine, index=False, if_exists='append')
receivers_data.to_sql('receivers', engine, index=False, if_exists='append')

engine.dispose()