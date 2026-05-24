sHPFC and variants:

$$
\begin{align}\partial_t \psi = \Gamma \nabla^2 \mu - \Gamma_J \mathcal{J}[\mathbf{v}, \psi]
\end{align}
$$

$$
\begin{align}
\rho_0 \partial_t \mathbf{v} = \nabla \cdot \mathcal{H} [\mu, \psi, f] + \Gamma_S \nabla^2 \mathbf{v}
\end{align}
$$

Advection variants:

$$
\begin{align}
\mathcal{J}_1[\mathbf{v}, \psi] = \mathbf{v} \cdot \nabla \psi
\end{align}
$$

$$
\begin{align}
\mathcal{J}_2[\mathbf{v}, \psi] = \nabla \cdot (\mathbf{v} \psi)
\end{align}
$$

Force variants:

$$
\begin{align}
\nabla \cdot \mathcal{H}_1[\mu, \psi, f] = \langle \mu \nabla \psi - \nabla f \rangle
\end{align}
$$

$$
\begin{align}
\nabla \cdot \mathcal{H}_2[\mu, \psi, f] = - \langle \psi \nabla \mu  \rangle
\end{align}
$$

Tiled video layout

$$
\begin{align}
a: \mathcal{J}_1, \mathcal{H}_1 &&| \quad b: \mathcal{J}_2, \mathcal{H}_1 \\
\hline
c: \mathcal{J}_1, \mathcal{H}_2 &&| \quad d: \mathcal{J}_2, \mathcal{H}_2 \\
\end{align}
$$

Model parameters

$$
\begin{align}
a: &\rho_0 = \Gamma_S = 2^{-6}, \Gamma_J = 1 \\
b: &\rho_0 = \Gamma_S = 2^{-6}, \Gamma_J = 10^{-1} \\
c: &\rho_0 = 200, \Gamma_S = 50, \Gamma_J = 1 \\
d: &\rho_0 = 200, \Gamma_S = 50, \Gamma_J = 1 \\
\end{align}
$$

