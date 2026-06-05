import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import requests

def main():
    jar = {
        "1gr" : {
            "amount" : 923,
            "weight" : 1516,
            "diameter" : 15.5,
            "height" : 1.4
        },
        "2gr" : {
            "amount" : 338,
            "weight": 723,
            "diameter" : 17.5,
            "height" : 1.4
        },
        "5gr" : {
            "amount" : 480,
            "weight": 1245,
            "diameter" : 19.48,
            "height" : 1.4
        },
        "total" : {
        }
    }
    jar = calc(jar)

    app, tabview = init_window()

    draw_efficiency_tab(tabview, jar)
    draw_wi_tab(tabview, jar)
    draw_gold_tab(tabview, jar)

    app.mainloop()

def calc(jar):
    #values
    jar["1gr"]["value"] = jar["1gr"]["amount"] / 100
    jar["2gr"]["value"] = jar["2gr"]["amount"] * 2 / 100
    jar["5gr"]["value"] = jar["5gr"]["amount"] * 5/ 100 
    for i in ["1gr", "2gr", "5gr"]:
        #radius
        jar[i]["radius"] = jar[i]["diameter"] / 2
        #volume
        jar[i]["volume"] = math.pi * math.pow(jar[i]["radius"], 2) * jar[i]["height"] * jar[i]["amount"]
    #totals init
    jar["total"]["amount"] = 0
    jar["total"]["value"] = 0
    jar["total"]["weight"] = 0
    jar["total"]["volume"] = 0
    #totals calc
    for i in ["1gr", "2gr", "5gr"]:
        jar["total"]["amount"] += jar[i]["amount"]
        jar["total"]["value"] += jar[i]["value"]
        jar["total"]["weight"] += jar[i]["weight"]
        jar["total"]["volume"] += jar[i]["volume"]
    
    #percentages
    for i in ["1gr", "2gr", "5gr"]:
        jar[i]["amount%"] = jar[i]["amount"] / jar["total"]["amount"] * 100
        jar[i]["value%"] = jar[i]["value"] / jar["total"]["value"] * 100
        jar[i]["weight%"] = jar[i]["weight"] / jar["total"]["weight"] * 100
        jar[i]["volume%"] = jar[i]["volume"] / jar["total"]["volume"] * 100        
    return jar

def init_window():
    app = ctk.CTk()
    app.title("Monetki")
    app.geometry("800x600")
    tabview = ctk.CTkTabview(master=app, width=750, height=550)
    tabview.pack(padx=20, pady=20)
    return app, tabview

def draw_efficiency_tab(tabview, jar):
    eff = tabview.add("Efficiency")

    fig, ax = plt.subplots(figsize=(9, 6)) 
    categories = ["Amount", "Value", "Weight", "Volume"]
    
    gr1_per = [jar["1gr"]["amount%"], jar["1gr"]["value%"], jar["1gr"]["weight%"], jar["1gr"]["volume%"]]
    gr2_per = [jar["2gr"]["amount%"], jar["2gr"]["value%"], jar["2gr"]["weight%"], jar["2gr"]["volume%"]]
    gr5_per = [jar["5gr"]["amount%"], jar["5gr"]["value%"], jar["5gr"]["weight%"], jar["5gr"]["volume%"]]
    start = [gr1_per[i] + gr2_per[i] for i in range(4)]

    c1 = ax.barh(categories, gr1_per, label="1gr", color="#cd7f32")
    c2 = ax.barh(categories, gr2_per, left=gr1_per, label="2gr", color="#b0c4de")
    c3 = ax.barh(categories, gr5_per, left=start, label="5gr", color="#ffd700")

    def make_labels(coin):
        return [
            f"{jar[coin]['amount%']:.0f}%\n({jar[coin]['amount']})",
            f"{jar[coin]['value%']:.0f}%\n({jar[coin]['value']:.2f})",
            f"{jar[coin]['weight%']:.0f}%\n({jar[coin]['weight']:.0f})",
            f"{jar[coin]['volume%']:.0f}%\n({jar[coin]['volume']/1000:.0f})"
        ]

    labels_1gr = make_labels("1gr")
    labels_2gr = make_labels("2gr")
    labels_5gr = make_labels("5gr")

    ax.bar_label(c1, labels=labels_1gr, label_type='center', color='white', fontweight='bold', fontsize=9)
    ax.bar_label(c2, labels=labels_2gr, label_type='center', color='black', fontweight='bold', fontsize=9)
    ax.bar_label(c3, labels=labels_5gr, label_type='center', color='black', fontweight='bold', fontsize=9)

    totals = [
        f"Total: {jar['total']['amount']} pcs",
        f"Total: {jar['total']['value']:.2f} PLN",
        f"Total: {jar['total']['weight']:.0f} g",
        f"Total: {jar['total']['volume']/1000:.0f} cm³" 
    ]

    ax.set_xlim(0, 120)
    
    for i, total_text in enumerate(totals):
        ax.text(102, i, total_text, va='center', fontweight='bold', fontsize=10)

    ax.set_xlabel("Share in %")
    ax.set_title("Jar efficiency: Share of denominations in different categories")
    ax.legend(loc="upper left") 

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=eff)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

def draw_wi_tab(tabview, jar):
    wi = tabview.add("What if?")
    
    total_weight = jar["total"]["weight"]
    weight_per_1gr = jar["1gr"]["weight"] / jar["1gr"]["amount"]
    weight_per_2gr = jar["2gr"]["weight"] / jar["2gr"]["amount"]
    weight_per_5gr = jar["5gr"]["weight"] / jar["5gr"]["amount"]

    sim_amount_1gr = int(total_weight / weight_per_1gr)
    sim_amount_2gr = int(total_weight / weight_per_2gr)
    sim_amount_5gr = int(total_weight / weight_per_5gr)

    sim_value_1gr = (sim_amount_1gr * 1) / 100
    sim_value_2gr = (sim_amount_2gr * 2) / 100
    sim_value_5gr = (sim_amount_5gr * 5) / 100

    base_categories = ["Normal jar", "Only 1gr", "Only 2gr", "Only 5gr"]
    amounts = [jar["total"]["amount"], sim_amount_1gr, sim_amount_2gr, sim_amount_5gr]
    values = [jar["total"]["value"], sim_value_1gr, sim_value_2gr, sim_value_5gr]

    categories = []
    for i in range(4):
        ratio = amounts[i] / values[i] 
        categories.append(f"{base_categories[i]}\n({ratio:.1f} pcs/PLN)")

    fig, ax1 = plt.subplots(figsize=(8, 4))

    ax2 = ax1.twinx()

    x = range(len(categories)) # [0, 1, 2, 3]
    width = 0.35

    x_amounts = [pos - width/2 for pos in x]
    x_values = [pos + width/2 for pos in x]

    c1 = ax1.bar(x_amounts, amounts, width, label="Amount (pcs)", color="#4682b4")
    c2 = ax2.bar(x_values, values, width, label="Value (PLN)", color="#cd7f32")

    ax1.bar_label(c1, padding=3, fmt='%.0f') 
    ax2.bar_label(c2, padding=3, fmt='%.2f')

    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.set_ylabel("Amount (pcs)", color="#4682b4", fontweight='bold')
    ax2.set_ylabel("Value (PLN)", color="#cd7f32", fontweight='bold')
    ax1.set_title("Simulation of the jar preserving the same weight")

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    ax1.set_ylim(0, max(amounts) * 1.2)
    ax2.set_ylim(0, max(values) * 1.2)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=wi)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

def get_gold():
    r_today = requests.get("https://api.nbp.pl/api/cenyzlota")
    today = r_today.json()[0]["cena"]
    r_past = requests.get(f"https://api.nbp.pl/api/cenyzlota/2018-01-02")
    past = r_past.json()[0]["cena"]
    return today, past
    
def calc_inflation(total_pln, today_price, past_price):
    gold_grams_past = total_pln / past_price
    gold_grams_today = total_pln / today_price
    
    value_if_invested = gold_grams_past * today_price
    lost_income = value_if_invested - total_pln
    
    return gold_grams_past, gold_grams_today, value_if_invested, lost_income

def draw_gold_tab(tabview, jar):
    gold_tab = tabview.add("Gold")

    today_price, past_price = get_gold()
    total_pln = jar["total"]["value"]
    
    gold_grams_past, gold_grams_today, value_if_invested, lost_income = calc_inflation(total_pln, today_price, past_price)

    frame = ctk.CTkFrame(master=gold_tab)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    title = ctk.CTkLabel(master=frame, text="Inflation factor on the jar of pennies (2018 vs 2026)", font=("Arial", 20, "bold"))
    title.pack(pady=15)
    
    label_past = ctk.CTkLabel(master=frame, text=f"In 2018, for {total_pln:.2f} zł you could have bought:\n{gold_grams_past:.3f} grams of gold", font=("Arial", 16))
    label_past.pack(pady=10)
    
    label_today = ctk.CTkLabel(master=frame, text=f"Today, for the same {total_pln:.2f} zł you can buy only:\n{gold_grams_today:.3f} grams of gold", font=("Arial", 16))
    label_today.pack(pady=10)
    
    conclusion = f"If you had bought gold in 2018, you would have had {value_if_invested:.2f} zł.\nThe Jar 'costed' you {lost_income:.2f} zł of lost income! :)"
    label_conclusion = ctk.CTkLabel(master=frame, text=conclusion, font=("Arial", 16, "bold"), text_color="#ff4444")
    label_conclusion.pack(pady=20)

if __name__ == "__main__":
    main()