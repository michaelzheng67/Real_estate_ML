import numpy as np

# function is default set to have time horizon of 40 years with monthly step size
# Returns numpy array
def simulate_brownian_motion(initial, mu, sigma, time=40, steps=480):

    # essentially just returns an array that represents a line graph of an initial value moving through time
    # with random variations (e.g like a stock chart line)
    dt = time / steps
    t = np.linspace(0, time, steps)
    w = np.random.standard_normal(size=steps)
    w = np.cumsum(w) * np.sqrt(dt)
    x = (mu - 0.5 * sigma ** 2) * t + sigma * w
    s = initial * np.exp(x)
    return s

def simulate_brownian_motion2(initial, mu, sigma, time=40, steps=480):

    # essentially just returns an array that represents a line graph of an initial value moving through time
    # with random variations (e.g like a stock chart line)
    dt = time / steps
    t = np.linspace(0, time, steps)
    w = np.random.standard_normal(size=steps)
    w = np.cumsum(w) * np.sqrt(dt)
    x = (mu - 0.5 * sigma ** 2) * t + sigma * w
    s = initial * np.exp(x)
    return s
