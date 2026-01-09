--Ride Trends:
SELECT "Booking_Date", COUNT(*) AS total_rides FROM public.ola GROUP BY "Booking_Date"
ORDER BY total_rides DESC;

--Booking Status:
SELECT "Booking_Status", COUNT(*) AS total_bookings FROM public.ola GROUP BY "Booking_Status";

--Total Customer Cancellations:
SELECT COUNT(*) AS Customer_Cancellations FROM public.ola WHERE "Booking_Status" = 'Canceled by Customer';

--Top 5 customers by rides:
SELECT "Customer_ID", COUNT(*) AS total_rides FROM public.ola GROUP BY "Customer_ID" 
ORDER BY total_rides DESC LIMIT 5;

--Driver Cancellation by reason:
SELECT "Canceled_Rides_by_Driver", COUNT(*) AS Total FROM public.ola GROUP BY "Canceled_Rides_by_Driver"
ORDER BY Total DESC;

--Max And Min Driver Ratings(Prime Sedan):
SELECT MAX("Driver_Ratings"::NUMERIC) AS max_rating, MIN("Driver_Ratings"::NUMERIC) AS min_rating FROM public.ola
WHERE "Vehicle_Type" = 'Prime Sedan' AND "Driver_Ratings" IS NOT NULL AND "Driver_Ratings" <> 'null';

--Rides paid using UPI:
SELECT * FROM public.ola WHERE "Payment_Method" = 'UPI';

--Average Customer Rating per Vehicle Type:
SELECT "Vehicle_Type", ROUND(AVG("Customer_Rating"::NUMERIC),2) AS Avg_Customer_Rating FROM public.ola
WHERE "Customer_Rating" IS NOT NULL AND "Customer_Rating" <> 'null' GROUP BY "Vehicle_Type";

--Total Booking Value:
SELECT SUM("Booking_Value"::NUMERIC) AS total_Revenue FROM public.ola WHERE "Booking_Status"='Success';

--Incomplete Rides With Reason:
SELECT "Booking_ID","Incomplete_Rides_Reason" FROM public.ola WHERE "Incomplete_Rides" = 'Yes';