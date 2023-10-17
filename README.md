# Argentine Primary Products Exports Prediction Model

This project focuses on developing a prediction model for Argentina's primary products exports. The dataset used covers the time series of export values in millions of USD from January 2005 to November 2022, with monthly frequency.

## Models Used

Two main models are employed for prediction:

1. **Ordinary Least Squares (OLS) Model:**
    - In this model, both exogenous and endogenous variables are considered.
    - Exogenous variables include product prices, precipitation data, and the real exchange rate.
    - The need for stationarity and autocorrelation management is addressed through differencing and incorporating lags.
    - The final model is estimated using multiple regressions to find the optimal lag structure for each variable.
    - The model provides a prediction that suggests a decrease in exports and quantifies the impact of exogenous factors.

2. **SARIMAX Model:**
    - The SARIMAX model is employed to tackle seasonality, stationarity, and serial correlation issues.
    - It considers the same exogenous variables as the OLS model.
    - Parameter calibration is done using the AIC method.
    - The model's accuracy is tested, and it provides predictions for future export values.

## Model Evaluation

- The OLS model helps predict a decline in exports and can be improved by including additional variables like the exchange rate gap.
- The SARIMAX model is promising, providing accurate predictions for certain periods. However, its effectiveness in forecasting future values is questioned, especially regarding severe events like droughts.

## Conclusion and Further Improvements

The project acknowledges the presence of "overfitting" issues and suggests that the model selection process should not rely solely on the lowest AIC but on the ability to make accurate predictions.

There is room for further refinement to enhance predictive accuracy.

