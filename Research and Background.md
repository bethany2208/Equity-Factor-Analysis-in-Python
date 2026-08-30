# Background and Research

## Reason For Project
I would like to have a better understanding of combining coding and quantitive statistics markets. I would like to understand what it is like to create a small quantitive research pipeline.
## Aim of the Project
To research whether simple factors such as momentum, value, and volatility explain differences in subsequent stock returns?
## Scope
Initially relativley small using around 50-100 large US equities, to simplify project I will be using constituents of the S&P 500, however it will be affected by survivorship bias.
## Factors
### 1: Momentum
This is how strongly the stock has performed recently.
This can be calculated by the following equation
$$ Momentum_t = \frac{Price_{t-21}}{Price_{t-252}} - 1$$
Where t is the point in time, this is approximatley the stocks return over the last year excluding the most recent month.
### 2: Value
We are going to use earnings yield, which effectivley means the higher the earnings yield the cheaper the stock. This can be calculated by the following equations:
$$ Earnings Yield = \frac{Earnings}{Price}$$
### 3: Volatillity
This will calculate the historical volatility, which is its tendency to change quickly. This can be calculated from its daily returns in the equation below.
$$ σ = Std(Returns) \times \sqrt{252}
