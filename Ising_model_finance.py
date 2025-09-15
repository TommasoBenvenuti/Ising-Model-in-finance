import os
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# -.-.-.-.-. Input -.-.-.-..-.
N_totale = 35
n_steps = 5000

# Parametri modificati secondo paper
alpha = 0.2
beta = 1.0    # Regime irrazionale
b_max = 0.05
sigma_max = 0.03
CV = 0.1
lambda_val = 40

# Inizializzazione 
J = np.zeros((N_totale, N_totale, n_steps))
epsilon = np.zeros((N_totale, N_totale))
b = np.zeros((N_totale, N_totale))
sigma = np.zeros((N_totale, N_totale))

for i in range(N_totale):
    for j in range(N_totale):
        b[i,j] = np.random.uniform(0, b_max)
        sigma[i,j] = np.random.uniform(0, sigma_max) 
        epsilon[i,j] = np.random.normal(0, CV + 0.1)

# Notizie globali 
G_global = np.random.normal(0, 1, n_steps)

# Inizializzazione grid  
Grid = np.random.choice([-1, 1], size=(N_totale, N_totale))

# Arrays per plotting 
xdata = [] 
sentiment = []
prices = [1.0]
returns = [0]  
volatility = []
observed_returns = []   

def compute_neighbors(Grid, posizione):
    i, j = posizione
    up = (i - 1) % len(Grid)
    down = (i + 1) % len(Grid)
    left = (j - 1) % len(Grid)
    right = (j + 1) % len(Grid)
    return (Grid[up,j] + Grid[down,j] + Grid[i,left] + Grid[i,right])

# figure: 1 riga x 3 colonne
fig, axes = plt.subplots(1, 3, figsize=(18, 10))

def update(step):
    global Grid
     
    prev_return = returns[-1] if len(returns) > 0 else 0
     
    i = random.randrange(N_totale)
    j = random.randrange(N_totale)
    selected_spin = Grid[i, j]
     
    # J-costant updates
    if step > 0:
        J[i, j, step] = b[i, j] + alpha * J[i, j, step-1] + beta * prev_return * G_global[step-1]
    else:
        J[i, j, step] = b[i, j]
    
    # Calcolo energia  
    DeltaS = -2 if selected_spin == 1 else +2
    neigh = compute_neighbors(Grid, (i, j))
    Q = (-J[i, j, step] * neigh + G_global[step]*sigma[i, j] + epsilon[i, j])* DeltaS
    # Metropolis
    if (Q < 0) or (random.random() < np.exp(-Q)):
        Grid[i, j] = -selected_spin

    # Sentiment
    S_avg = np.sum(Grid)/(N_totale**2)
    sentiment.append(S_avg)
    xdata.append(step)
    
    # Returns e prezzi
    current_return = S_avg/lambda_val if step > 1 else 0
    returns.append(current_return)
    price = prices[step-1] * np.exp(current_return) if step > 0 else prices[0]
    
    #Debug
    #print(f"Step {step}: Price = {price}, Return = {current_return}, Sentiment = {S_avg}")
    
    prices.append(price)

    
     
    # Volatilità
    window_size = 30
    if step >= window_size:
        recent_returns = returns[-window_size:]
        volatility_val = np.std(recent_returns)
    else:
        volatility_val = 0
    volatility.append(volatility_val)

    observed_returns.append(np.log(prices[-1])/(prices[-2]) if step > 1 and prices[-2] > 0 else 0)

    # ===== Aggiornamento grafici =====
    axes[0].cla()
    xSpin, ySpin, colors = [], [], []
    for i in range(N_totale):
        for j in range(N_totale):
            xSpin.append(i)
            ySpin.append(j)
            colors.append('red' if Grid[i,j] == -1 else 'blue')
    axes[0].scatter(xSpin, ySpin, c=colors, s=20)
    axes[0].set_title(f"Spin Configuration ")
    axes[0].set_xlim(0, N_totale)
    axes[0].set_ylim(0, N_totale)
    axes[0].set_aspect('equal')



    # Prezzo
    axes[1].cla()
    axes[1].plot(xdata, prices[1:], 'b-')
    axes[1].set_xlabel("Steps")
    axes[1].set_ylabel("Price")
    axes[1].set_title("Market Price")
    
    axes[2].cla()    
    axes[2].plot(returns, 'r-', label='Expected from Market Sent.')
    axes[2].set_title("Returns")
    axes[2].legend()
    axes[2].set_xlabel("Steps")
    # Configurazione spin

# Animazione

ani = FuncAnimation(fig, update, frames=n_steps, repeat=False)

# Salvataggio in MP4
writer = FFMpegWriter(fps=150, bitrate=3000)
ani.save("ising_market_full.mp4", writer=writer)


print("Video salvato come ising_market_full.mp4")

