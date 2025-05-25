# Add a mixin class to handle axis styling for matplotlib plots

class AxisStylingMixin:
    def set_axis_styling(self, ax):
        ax.grid(True, linestyle=':', linewidth=0.8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', rotation=45)
