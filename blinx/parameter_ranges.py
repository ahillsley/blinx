import jax.numpy as jnp

from .parameters import Parameters


class ParameterRanges:
    """Min/max and number of values to explore by the optimizer.

    Args:

        mu_range (tuple):

            The min and max mean intensity values of a single emitter
            to grid search over

        mu_bg_range (tuple):

            The min and max background intensity values
            to grid search over

        sigma_range (tuple):

            The min and max values of the std of the intensity of a single emitter
            to grid search over

        p_on_range (tuple):

            the min and max p_on values to grid search over

        p_off_range (tuple):

            the min and max p_on values to grid search over

        mu_step (int):

            The number of values to grid search over for :class:`Parameters`
            `mu`

        mu_bg_step (int):

            The number of values to grid search over for :class:`Parameters`
            `mu_bg`

        sigma_step (int):

            The number of values to grid search over for :class:`Parameters`
            `sigma`

        p_on_step (int):

            The number of values to grid search over for :class:`Parameters`
            `p_on`

        p_off_step (int):

            The number of values to grid search over for :class:`Parameters`
            `p_on`
    """

    def __init__(
        self,
        r_e_range=(100, 30000),
        r_bg_range=(5000, 5000),
        mu_ro_range=(1000, 3000),
        sigma_ro_range=(0.1, 0.1),
        gain_range=(1, 3),
        p_on_range=(1e-4, 1.0),
        p_off_range=(1e-4, 1.0),
        r_e_step=100,
        r_bg_step=1,
        mu_ro_step=1,
        sigma_ro_step=1,
        gain_step=1,
        p_on_step=20,
        p_off_step=20,
    ):
        self.r_e_range = Range(*r_e_range, r_e_step)
        self.r_bg_range = Range(*r_bg_range, r_bg_step)
        self.mu_ro_range = Range(*mu_ro_range, mu_ro_step)
        self.sigma_ro_range = Range(*sigma_ro_range, sigma_ro_step)
        self.gain_range = Range(*gain_range, gain_step)
        self.p_on_range = Range(*p_on_range, p_on_step)
        self.p_off_range = Range(*p_off_range, p_off_step)

        if self.p_on_range.start is None:
            self.p_on_range.start = 1e-4
        if self.p_off_range.start is None:
            self.p_off_range.start = 1e-4
        if self.p_on_range.stop is None:
            self.p_on_range.stop = 1.0
        if self.p_off_range.stop is None:
            self.p_off_range.stop = 1.0

    def num_values(self):
        return tuple(
            r.step
            for r in [
                self.r_e_range,
                self.r_bg_range,
                self.mu_ro_range,
                self.sigma_ro_range,
                self.gain_range,
                self.p_on_range,
                self.p_off_range,
            ]
        )

    def to_parameters(self):
        range_tensors = {
            "r_e": self.r_e_range.to_tensor(),
            "r_bg": self.r_bg_range.to_tensor(),
            "mu_ro": self.mu_ro_range.to_tensor(),
            "sigma_ro": self.sigma_ro_range.to_tensor(),
            "gain": self.gain_range.to_tensor(),
            "p_on": self.p_on_range.to_tensor(),
            "p_off": self.p_off_range.to_tensor(),
        }

        values = {
            name: v.flatten()
            for name, v in zip(
                range_tensors.keys(),
                jnp.meshgrid(*range_tensors.values(), indexing="ij"),
            )
        }

        return Parameters(**values)


class Range:
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step

    def to_tensor(self):
        return jnp.linspace(self.start, self.stop, self.step)
