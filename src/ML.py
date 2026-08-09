import pandas as pd
from .Prediction import train_linear_model



def predict_car_price(horsepower, engine_size, curb_weight, city_mpg, fuel_type,df_processed):
        model, features = train_linear_model(df_processed)
        
        city_l_100km = 235 / city_mpg
        fuel_gas = 1 if fuel_type == "Gas" else 0
        fuel_diesel = 1 if fuel_type == "Diesel" else 0

        input_data = pd.DataFrame(
            [[horsepower, engine_size, curb_weight, city_l_100km, fuel_gas, fuel_diesel]],
            columns=features,
        )
        prediction = model.predict(input_data)
        return f"Estimated Market Value: ${prediction[0]:,.2f}"