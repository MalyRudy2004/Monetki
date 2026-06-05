# Monetki (Coinies)
## Description:

### Introduction
In Poland, there are a few types of coins:
* **1zł, 2zł and 5zł** (1zł ≈ $0.25) - The ones you actually want in your wallet.
* **10gr, 20gr and 50gr** (1gr = 1/100 zł) - Pretty annoying but still worth carrying. They are silver in color.
* **1gr, 2gr and 5gr** - The money no one wants, nearly worthless. If a cashier doesn't have the exact change, you just say it's okay and leave. Their color is similar to copper and that's why they are called "miedziaki" (copper in Polish is *miedź*) despite they are not really made from copper.

### Motivation
"Miedziaki" can be found outside lying on the sidewalk, behind the couch in the living room, or in an old wallet. I always wondered how much money people lose by underestimating those coins! That's why in 2018, while in secondary school, I took an empty jar and started collecting those pennies. It took me around 7 years to fill the jar, but it was worth it – I gathered a substantial amount of coins to prepare a comparison and analysis.

The problem was that my primary programming language was C. That's why I started this course (I initially tried drawing charts in C, but it was not a pleasant experience!).

### The Process
I decided to create a GUI application using the `customtkinter` and `matplotlib` libraries and placed 3 tabs inside:
* **Analysis:** The first tab shows the raw data – how many of which coin there are, and their share in total weight, amount, and volume.
* **What if?:** The second tab simulates what the total value would be if there were only one type of coin in the jar (e.g., 1gr only) while maintaining the exact same physical weight.
* **The Time Machine:** In the last tab, I tried to measure if hoarding this money has real consequences and how inflation fluctuates over the years. I compare the price of gold and calculate how much of it I could buy with the exact same amount of money in 2018 versus 2026. The live data is fetched from the NBP API (National Bank of Poland).

### The Results
Concluding, there isn't an easy answer to the main question.
* **Is it a lot of money?** - No.
* **Did it lose its worth over time?** - Yes, but so did the 1zł coin and the 100zł bill.
* **Was it a valuable experiment?** - Yes, it was fun and I learned Python! :)

The ultimate solution to this problem: Don't hide those coins! Try to spend them regularly. Rather than paying a full 1zł for something that costs 0.74zł, you can give the cashier 50gr + 20gr + 2gr + 2gr. The queue in the store won't be mad for waiting an additional 20 seconds.

*Fun fact: All the money from the jar was donated to WOŚP (The Great Orchestra of Christmas Charity), which is the biggest Polish fundraiser that collects money every year for medical equipment for children's hospitals.*

---

## The code itself

### Data allocation
Gathered data from the jar was:
* Amount of coins of each type
* Weight of coin type groups
* The dimensions were taken from the wikipedia

I decided to use dictionary of dictionaries for storing the data. At first, I wanted to create a class, but the dictionary allowed me to segregate the data in more visible way than one class Jar could.
I also added the empty dict "total" which was to be calculated on the fly.

### `calc`
The first function is the calc function which is responsible for simple operations. Calculation of total values, weights and volumes for particular group of coins, also their share in percents.

### `init_window`
This function initializes the tkinter's library app funtions and creates the variables:
* **app** - which is the application widnow itself
* **tabview** - which holds the data for application tabs and allows to create new ones

### `draw_efficiency_tab`
This function takes the parameter **tabview** to create a new tab, eff (efficiency). In this tab there are 4 charts showing the share in percents of each coin group in each category:
* Weight
* Volume
* Amount
* Value

For displaying the charts I decided on using the Matplotlib library, as I found it pretty beginner friendly with many tutorials and documentation examples. I created the lists with labels and data for the axes. Because the work was repeatable, I tried to create a function inside a function (make_labels) which worked well and from the time perspective I think I should have done that more often.
This library allowed me to add the legend and place it in the desired space with single methods.

### `What_if`
This function similarily creates a new tab, but this time basing on the total weight of collected coins and the weight of single coin of each type calculates the prediction of how many coins of each type would fit in the jar. This is presented in double bar chart in a format amount/value to show the power of the coins.
The process of creating additional axis and bar chart was again pretty handy and intuitive.

### `get_gold`
This function uses the request library to use the NBP (National Bank of Poland) API. It is used twice:
* Firstly, for the fixed date of 2nd of January, 2018 - as I set it as a reference point of starting the coins collection (The second was chosed because on the holidays, the api does not update, therefore the requests cannot download any data and ends with error)
* Secondly, for the usage day - The problem with holidays does not work here because without specifying the date, we get the latest update of the API

The taken data is in format of JSON, from where the gold value is extracted and returned from the function.
I thought that comparing the jar worth to the gold price would be the best way of showing the inflation across the years.

### `calc_inflation`
Simple function that basing on the past and todays prices calculates the inflation and potentially lost income of what we could earn if we had invested in gold years earliel (which actually does not make much sense because I couldn't have invested the money that I comleted collecting now).

### `draw_gold_tab`
This is the last tab creating function. There is no charts but there is a frame with text. It says what is the gold price and how much gold you can buy now and could have bought back then. Then pessimistically tells you how much you "lost" by not investing :)

### The `main` function
Because all of the calculations, tab creations and chart drawing takes place inside specific functions, the main is limited to calling them in a correct order. At the end it calls `app.mainloop()` and the window appears.
