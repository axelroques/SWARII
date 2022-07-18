# Sliding Window Average with Relevance Interval Interpolation (`SWARII`)

Python implementation of the SWARII algorithm from _Audiffren & Contal (2016)_, adapted from the authors' code.

## Important note(s)

The original paper erroneously defines the _Relevance Interval_ (RI), which is the key contribution compared to the Sliding Window Average Interpolation (`SWAI`) method. The article states the following.

_Relevance Interval_. Let $s$ be a time instant, $\Delta$ be a time duration and $T_s(\Delta) = \left\{t \in T , |t − s| ≤ \Delta\right\}$ be a window centered around $s$. We denote by $t_p, . . . , t_q$ the ordered timestamps in $T_s(\Delta)$. Then, for every $t_i \in T_s(\Delta)$ we define $I_{T_s}(\Delta)(t_i)$ the relevance interval of $t_i$ in the window:

$
\begin{equation}
I_{T_s}(\Delta)(t_i) = \begin{cases} 
\frac{1}{2}(t_{i+1} - t_{i-1}), \qquad \qquad\text{ for } p < i < q \\
\frac{1}{2}(t_{i+1}-t_i)-(s-\Delta), \;\text{ for } i = p \\
s+\Delta-\frac{1}{2}(t_i-t_{i-1}), \quad\text{ for } i = q \\
\end{cases}
\end{equation}
$

With this definition, the `SWARII` method evaluates the value at a desired time $s$ using the following formula
$
\begin{equation}
X_{\text{SWARII}}(s) = \frac{1}{\Delta} \sum_{t_i \in T_s(\Delta)} x_{t_i} I_{T_s}(\Delta)(t_i)
\end{equation}
$

Basically, the value at timestamp s is computed as a weighted average of every point in the relevance interval, _i.e._ a temporal window centered around s of length $2\Delta$ - the article mentions a length of $\Delta$ which I assume is a mistake.

The authors also assert that
$
\begin{equation}
\sum_{t_i \in T_s(\Delta)} I_{T_s}(\Delta)(t_i) = \Delta
\end{equation}
$

This, however, is not true. Using the first equation, we find that
$
\begin{equation}
\sum_{t_i \in T_s(\Delta)} I_{T_s}(\Delta)(t_i) = t_{q-1}-t_0 + 2\Delta
\end{equation}
$
a result that I verified consistently in a first version of the code.

The correct version of the first equation should be
$
\begin{equation}
I_{T_s}(\Delta)(t_i) = \begin{cases} 
\frac{1}{2}(t_{i+1} - t_{i-1}), \qquad \qquad\text{ for } p < i < q \\
\frac{1}{2}(t_{i+1}+t_i)-(s-\Delta), \;\text{ for } i = p \\
s+\Delta-\frac{1}{2}(t_i+t_{i-1}), \quad\text{ for } i = q \\
\end{cases}
\end{equation}
$

In that case, we obtain
$
\begin{equation}
\sum_{t_i \in T_s(\Delta)} I_{T_s}(\Delta)(t_i) = 2\Delta
\end{equation}
$
which is still not what is put forward by the authors but is consistent with the confusion mentioned above between the length of the temporal window and $\Delta$.

Also, equation (2) is inacurrate for the boundary conditions. More precisely, the cardinality of $T_s(\Delta)$ is not constant and depends on the time instant $s$ considered, _e.g._ when $s=0$ its cardinality is roughly half of its maximum expected cardinality. A more general formulation may be written as
$
\begin{equation}
X_{\text{SWARII}}(s) = \frac{1}{\sum_{t_i \in T_s(\Delta)} I_{T_s}(\Delta)(t_i)} 
\sum_{t_i \in T_s(\Delta)} x_{t_i} I_{T_s}(\Delta)(t_i)
\end{equation}
$

These corrections were implemented in this implementation.
