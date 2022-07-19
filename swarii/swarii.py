
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class SWARII:

    def __init__(self, data, window_size=1, fs=25):
        """
        Instantiate SWARII method.

        Input:
            - data = input data to resample. Should be a pandas
            DataFrame containing a 't' column with the timestamps
            of the potentially multidimensional signal.
            - window_size = size of the sliding window, in s.
            - desired_frequency = output sampling frequency 
            for the output signal after resampling, in Hz.
        """

        # Input parameters
        self.data = data
        self.window_size = window_size
        self.fs = fs

        # Working parameters
        self._t = self.data['t'].to_numpy()
        self._s = self.data.iloc[:, 1:].to_numpy()

    def process(self):
        """
        Run SWARII method.
        """

        # Resample
        t_out, s_out = self._resample()

        # Store results
        data_dict = {
            name: values for name, values in zip(
                self.data.columns[1:],
                s_out.T
            )
        }
        self._out = pd.DataFrame(
            data={
                't': t_out,
                **data_dict
            })

        return

    def get_results(self):
        """
        Return a new dataframe with the resampled signals.
        """
        return self._out

    def plot(self):
        """
        Plot results.
        """

        assert isinstance(self._out, pd.DataFrame), \
            "Run process() method first."

        n_rows = self._s.shape[1]
        _, axes = plt.subplots(n_rows, 1, figsize=(12, 2.5*n_rows))

        for i, ax in enumerate(axes.ravel()):
            ax.plot(self._t, self._s[:, i],
                    label=f'Original {self.data.columns[i+1]}',
                    c='royalblue', alpha=0.8)
            ax.plot(self._out['t'], self._out.iloc[:, i+1],
                    label=f'Resampled {self.data.columns[i+1]}',
                    c='crimson', alpha=0.8)
            ax.legend()

        plt.tight_layout()
        plt.show()

        return

    def _resample(self):
        """
        Resample a given signal.

        Input:
            - t = the time stamps of signal.
            - s = the signal to be resampled. (n, k) numpy array.

        Output: 
            - t_out = time stamps of the signal after the resampling.
            - s_out = the resampled signal.
        """

        # Time instant s, using the - debatable - notations
        # of the article
        s = self._t[0]
        delta = 0.5*self.window_size

        t_out = []
        s_out = []

        # Iterate over the time stamps
        while s < self._t[-1]:

            # Get relevance interval (RI)
            RI = [
                i for i in range(len(self._t))
                if abs(self._t[i]-s) < delta
            ]

            if len(RI) >= 2:
                norm = 0
                value = np.zeros((1, self._s.shape[1]))

                # Compute the signal value at time s, using the RI
                for i in RI:

                    # Left border case
                    if i == RI[0]:
                        I = 0.5*(self._t[i+1]+self._t[i]) - (s-delta)
                    # Right border case
                    elif i == RI[-1]:
                        I = (s+delta) - 0.5*(self._t[i]+self._t[i-1])
                    # Other cases
                    else:
                        I = 0.5*(self._t[i+1]-self._t[i-1])

                    norm += I
                    value += self._s[i] * I

            else:
                if len(RI) == 0:
                    s += 1./self.fs
                    continue
                if len(RI) == 1:
                    value = np.zeros((1, self._s.shape[1]))
                    value += self._s[RI[0]]
                    norm = 1

            value /= norm

            t_out.append(s)
            s_out.append(value)

            s += 1./self.fs

        return np.array(t_out), np.concatenate(s_out)
