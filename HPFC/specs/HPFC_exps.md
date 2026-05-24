Consistent Hydrodynamics for Phase Field Crystals [excluding amplitude expansion]:

$$
\begin{align}
\tilde{\mathcal{H}}[\tilde{\rho}, \tilde{\mathbf{v}}] &= T[\tilde{\rho}, \tilde{\mathbf{v}}] + \tilde{F}[\tilde{\rho}] \\
T[\tilde{\rho}, \tilde{\mathbf{v}}] &= \int d \mathbf{r} \left( \frac{1}{2} \rho |\mathbf{v}|^2 \right) \\
\partial_t \tilde{\rho} &= - \nabla \cdot (\tilde{\rho}\tilde{\mathbf{v}}) \\
\partial_t (\tilde{\rho}\tilde{\mathbf{v}}) &= - \nabla \cdot (\tilde{\rho}\tilde{\mathbf{v}} \otimes \tilde{\mathbf{v}}) + \tilde{\mathbf{f}} \\
\mathbf{f} &= -\rho \nabla \frac{\delta F}{\delta \rho}  \\
\tilde{F} &= \int d \mathbf{r} \left[ \frac{1}{2} (B^x \tilde{\rho} \mathcal{L} \tilde{\rho} + \Delta B \tilde{\rho}^2) + \frac{1}{3}g \tilde{\rho}^3 + \frac{1}{4} v_0 \tilde{\rho}^4 \right] \\
\rho \frac{D \mathbf{v}}{Dt} &= \langle \mathbf{f} \rangle + \mu_S \nabla^2 \mathbf{v} + (\mu_B - \mu_S) \nabla \nabla \cdot \mathbf{v} \\
\frac{D}{D t} &= \frac{\partial}{\partial t} + \mathbf{v} \cdot \nabla \\
\partial_t \rho &= - \nabla \cdot (\rho \mathbf{v}) + \mu_\rho \nabla^2 \frac{\partial \mathcal{H}}{\partial \rho}
\end{align}
$$

Final equations [density field $\psi$, dissipation coefficient $\mu_X \rightarrow \Gamma_X$]:
$$
\begin{align}
\partial_t \psi = \Gamma_\rho \nabla^2 \left( \mu + \frac{1}{2} |\mathbf{v}|^2 \right) - \nabla \cdot (\psi \mathbf{v}) \\
\rho_0 \partial_t \mathbf{v} = \langle - \psi \nabla \mu \rangle + \Gamma_S \nabla^2 \mathbf{v} - \rho_0 \mathbf{v} (\nabla \cdot \mathbf{v}) \\
\mu = (\nabla^2 + {q_0}^2)^2 \psi + r \psi + g \psi^2 + v_0 \psi^3
\end{align}
$$
