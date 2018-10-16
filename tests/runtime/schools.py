import pystan
import numpy as np
import matplotlib.pyplot as plt
import yaps

schools_code = """
data {
    int<lower=0> J; // number of schools
    real y[J]; // estimated treatment effects
    real<lower=0> sigma[J]; // s.e. of effect estimates
}
parameters {
    real mu;
    real<lower=0> tau;
    real eta[J];
}
transformed parameters {
    real theta[J];
    for (j in 1:J)
        theta[j] = mu + tau * eta[j];
}
model {
    eta ~ normal(0, 1);
    y ~ normal(theta, sigma);
}
"""

# Round Trip from Stan to Yaps to Stan
yaps_code = yaps.from_stan(code_string=schools_code)
schools = yaps.to_stan(yaps_code)

# Add Data
schools_dat = {'J': 8,
               'y': [28,  8, -3,  7, -1,  1, 18, 12],
               'sigma': [15, 10, 16, 11, 9, 11, 10, 18]}

# Compile and fit
sm = pystan.StanModel(model_code=str(schools))
fit = sm.sampling(data=schools_dat, iter=1000, chains=4)


# Visualize
print(fit)
eta = fit.extract(permuted=True)['eta']
np.mean(eta, axis=0)

# if matplotlib is installed (optional, not required), a visual summary and
# traceplot are available
fit.plot()
plt.show()

