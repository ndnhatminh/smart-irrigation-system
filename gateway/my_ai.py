# import pandas as pd
# df=pd.read_csv('data.csv',index_col='Date',parse_dates=True)
# df=df.dropna()
# print('Shape of data',df.shape)
# df.head()
# df
#

# print(df.shape)
# train=df.iloc[:-30]
# test=df.iloc[-30:]
# print(train['Temp'])
# print(train.shape,test.shape)
# from statsmodels.tsa.arima.model import ARIMA
# model=ARIMA(train['Temp'],order=(1,0,5))
# model=model.fit()
# model.summary()
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima


class ForecastModel:
    def __init__(self, csv_file, name) -> None:
        # Read the CSV file
        self.csv_file = csv_file  # Path to your CSV file
        self.data = pd.read_csv(csv_file, parse_dates=[
                                'Date'], index_col='Date')
        self.name = name

    def determine_parameter(self):
        stepwise_fit = auto_arima(
            self.data[self.name], trace=True,  suppress_warnings=True)
        print(stepwise_fit)

    def create_model(self, p, d, q):
        # Fit the ARIMA model
        model = ARIMA(self.data[self.name], order=(p, d, q))
        self.model_fit = model.fit()

    def forecasting(self, forecast_steps):
        # Forecast the next 15 seconds
        self.forecast = self.model_fit.forecast(steps=forecast_steps)

    def draw_figure(self, forecast_steps, save_in="D:\\phong.png"):
        # Create a new time index for the forecast
        forecast_index = pd.date_range(
            start=self.data.index[-1], periods=forecast_steps + 1, freq='S')[1:]
        # Plot the results
        plt.figure(figsize=(10, 5))
        plt.plot(self.data.index, self.data['Temp'], label='Observed')
        plt.plot(forecast_index, self.forecast, label='Forecast', color='red')
        plt.xlabel('Time')
        plt.ylabel(f'{self.name}')
        plt.title(f'{self.name} Forecast for the {forecast_steps} Next Seconds')
        plt.legend()
        plt.savefig(f'{save_in}')
        plt.show(block=False)

    def verification(self, value):
        # Print the forecasted values
        predicted_data = self.forecast.to_list()[0]
        print("Predicted data: ", predicted_data, "-------")
        if predicted_data > value:
            percentage = value/predicted_data
        else:
            percentage = predicted_data/value
        if percentage < 0.5:
            print(
                f"Percentage of {self.name} forecasting is too low, please recheck sensors or model")

    def retrain(self):
        self.create_model(0, 1, 0)


temperature_model = ForecastModel("data.csv", "Temp")
# temperature_model.determine_parameter("Temp")
temperature_model.create_model(0, 1, 0)
temperature_model.forecasting(15)
temperature_model.draw_figure(15)
temperature_model.verification(1)

humidity_model = ForecastModel("data.csv", "Humid")
# humidity_model.determine_parameter("Humid")
humidity_model.create_model(0, 1, 0)
humidity_model.forecasting(15)
humidity_model.draw_figure(15, "D:\\phong1.png")
humidity_model.verification(20)
