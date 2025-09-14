# Financial Market Simulation (Ising Model Inspired)

This project implements a financial market simulation based on the Ising model,  
where market agents (represented as spins in a grid) interact with each other and respond to global news, influencing price movements.

The model is based on:  
**Zhou, W.X., Sornette, D.** *Self-organizing Ising model of financial markets*. Eur. Phys. J. B 55, 175–181 (2007).  
[https://doi.org/10.1140/epjb/e2006-00391-6](https://doi.org/10.1140/epjb/e2006-00391-6)

 The implementation differs slightly from the article:  
 The Ising problem here is solved with the **Metropolis Monte Carlo** method (MCMC).

---

##  Theoretical Model

The simulation combines:
- **Ising model**: Agents (spins) can buy ($+1$) or sell ($-1$), analogous to spin-up or spin-down states.
- **Social influence**: Agents are influenced by their 4 nearest neighbors, analogous to spin exchange in Ising Model
- **Global news**: An external factor influencing all agents simultaneously. Something similar can be implemented in Ising model to simulate perturbation by magnetic Fields.
- **Agent heterogeneity**: Individual parameters ($b$, $\sigma$, $\epsilon$) define different behaviors.

The grid is initialized randomly.  
The **average spin value** at the first step determines the initial price (the market makes the price).

---

##  Key Equations

**Influence update**

$$
J_{i,j,t} = b_{i,j} + \alpha J_{i,j,t-1} + \beta r_{t-1} G_{t-1}
$$

- $b_{i,j}$: fixed parameter drawn from a uniform distribution in $(0, b_{\max})$  
- $J_{i,j,t-1}$: influence constant at previous step  
- $G_{t-1}$: global noise term  
- $r_{t-1}$: return at previous step  

---

**State transition (Metropolis)**

$$
\Delta S =
\begin{cases}
-2 & \text{if spin = +1} \\
+2 & \text{if spin = -1}
\end{cases}
$$

$$
Q = -J_{i,j,t} \cdot \text{neighbors} \cdot \Delta S
    + G_t \cdot (\sigma_{i,j} + \epsilon_{i,j}) \cdot \Delta S
$$

---

**Prices and Returns**

$$
R_t = \frac{S_{\text{avg}}}{\lambda}
$$

$$
P_t = P_{t-1} \cdot \exp(R_t)
$$

- $S_{\text{avg}}$: average spin value  
- $\lambda$: liquidity factor (higher liquidity → more stable market)

---

##  Parameters

You can vary them. Most of them are simply extracted from the article

- `N_total`: Grid size (35×35 agents)  
- `n_steps`: Number of iterations (50,000)  
- `alpha`: Persistence factor (0.2)  
- `beta`: Return sensitivity (1.0, irrational regime)  
- `b_max, sigma_max`: Limits for agent heterogeneity  
- `CV`: Coefficient of variation for noise  
- `lambda_val`: Scaling factor for returns (40)  

---

##  Output

The simulation generates:
- Real-time visualization of spin configuration (saved as `.mp4`)  
- Market price movement over time  
- Expected returns based on average sentiment  
