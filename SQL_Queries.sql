use Food_Management
--1st
select City, count(Name) as Provider_Count 
from providers 
group by City;
select City, count(Name) as Receiver_Count 
from receivers 
group by City;

--2nd
select Type,count(Name)as Total
from providers
group by Type
order by Total desc ;

--3rd
SELECT Name, Contact
FROM providers
WHERE City = 'New Jessica';

--4th
select Name, count(Receiver_ID) as Total
from(
select rc.Name , cl.Receiver_ID
from receivers rc
join claims cl 
on rc.Receiver_ID = cl.Receiver_ID) as tables
group by Name
order by Total desc;

--5th
select sum(Quantity) from food_listings;

--6th
select top 1 City , sum(Quantity) as Total
from
(select pd.City, fl.Quantity
from providers pd
join food_listings fl
on pd.Provider_ID = fl.Provider_ID) as tables
group by City
order by Total desc;

--7th
select Food_Type, count(Meal_Type) as Count
from food_listings
group by Food_Type
order by Count desc;

--8th
select Food_Name, count(Claim_ID) as Total_Claims
from
(select fl.Food_Name, cm.Claim_ID
from food_listings fl
join claims cm
on fl.Food_ID = cm.Food_ID) as tables
group by Food_Name
order by Total_Claims desc;

--9th
select top 1 Name, count(Status) as Highest_Claims
from
(select pd.Name, cm.Status
from providers pd
join food_listings fl 
on pd.Provider_ID =fl.Provider_ID
join claims cm
on fl.Food_ID = cm.Food_ID
where cm.Status = 'Completed') as tables
group by Name
order by Highest_Claims desc;

--10th
select Status,
 cast(Count(Claim_ID) as float)*100 /(select count(*) from claims)
as [Status%]
from Claims
group by Status;

--11th
select rv.Name as Receiver_Name, avg(fl.Quantity) as Avg_Quantity
from receivers rv
join claims cm 
on rv.Receiver_ID = cm.Receiver_ID
join food_listings fl
on fl.Food_ID = cm.Food_ID
group by rv.Name
order by Avg_Quantity desc;

--12th
select fl.Meal_Type, count(cm.Status) as Count 
from claims cm
join food_listings fl
on cm.Food_ID = fl.Food_ID
group by fl.Meal_Type
order by Count desc;

--13th
select pd.Name , sum(fl.Quantity) as Total_Qunatity 
from providers pd 
join food_listings fl 
on pd.Provider_ID = fl.Provider_ID
group by pd.Name
order by Total_Qunatity desc;

--14th
select fl.Food_ID, fl.Food_Name, cm.Timestamp as Claim_Date, fl.Expiry_Date 
from claims cm 
join food_listings fl 
on cm.Food_ID = fl.Food_ID

--15th
select rc.Type as Receiver_Type , sum(fl.Quantity) as Total_Quantity
from receivers rc
join claims cm
on rc.Receiver_ID = cm.Receiver_ID
join food_listings as fl
on cm.Food_ID = fl.Food_ID
group by rc.Type
order by Total_Quantity desc;