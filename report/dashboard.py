from fasthtml.common import *
import matplotlib.pyplot as plt
from employee_events import Employee, Team
from utils import load_model
from base_components import Dropdown, BaseComponent, Radio, MatplotlibViz, DataTable
from combined_components import FormGroup, CombinedComponent

# Custom dropdown for picking a report subject (employee or team)
class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model, *args, **kwargs):
        self.label = model.name  # Use the model name as the label
        return super().build_component(entity_id, model, *args, **kwargs)

    def component_data(self, entity_id, model, *args, **kwargs):
        return model.names()  # Just give us a list of names to populate the dropdown


# Logo and page title up top
class Header(BaseComponent):
    def build_component(self, entity_id, model, *args, **kwargs):
        logo_url = "https://iili.io/38ibE8J.jpg"
        return Div(cls="page-header")(
            Img(
                src=logo_url,
                alt="My Logo",
                style="display: block; margin-left: auto; margin-right: auto; height: 500px; width: auto;"
            ),
            H1(model.name)
        )


# Line chart to visualize how event counts stack up over time
class LineChart(MatplotlibViz):
    def visualization(self, asset_id, model, *args, **kwargs):
        df = model.event_counts(asset_id).fillna(0)
        df = df.set_index("event_date").sort_index().cumsum()
        df.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots(figsize=(12, 8))
        df.plot(ax=ax, color=['green', 'red'], linestyle='--', marker='o', linewidth=2)

        ax.set_title("Events of the Employees", fontsize=25, fontweight='bold', color='navy')
        ax.set_xlabel("Date", fontsize=20, color='purple')
        ax.set_ylabel("Cumulative Events (Count)", fontsize=25, color='purple')

        ax.grid(True, linestyle=':', linewidth=0.8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', rotation=45)

        ax.legend(title="Event Type", fontsize=12, title_fontsize=14)

        self.set_axis_styling(ax)
        return fig


# Bar chart that shows how risky recruitment is for a given employee or team
class BarChart(MatplotlibViz):
    predictor = load_model()  # Load the prediction model just once

    def visualization(self, asset_id, model, *args, **kwargs):
        probas = self.predictor.predict_proba(model.model_data(asset_id))[:, 1]
        pred = probas.mean() if model.name == "team" else probas[0]

        fig, ax = plt.subplots(figsize=(8, 3))
        fig.suptitle("Recruitment Risk Prediction", fontsize=20, fontweight='bold', color='navy')

        bar_color = 'green' if pred < 0.3 else 'orange' if pred < 0.6 else 'red'
        ax.barh([0], [pred], color=bar_color, edgecolor='black', height=0.4)

        text_x = pred / 2 if pred > 0.1 else pred + 0.02
        text_color = 'white' if pred > 0.1 else 'black'
        ha = 'center' if pred > 0.1 else 'left'

        ax.text(text_x, 0, f"{pred:.1%}", va='center', ha=ha, fontsize=12, color=text_color, fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, 0.5)
        ax.get_yaxis().set_visible(False)
        ax.set_xlabel("Risk Probability", fontsize=15, color='purple')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)

        self.set_axis_styling(ax)
        return fig


# A tidy bundle of both visualizations
class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls="grid")


# Just a simple notes table – think of it like comment logs
class NotesTable(DataTable):
    def component_data(self, entity_id, model, *args, **kwargs):
        return model.notes(entity_id)


# These are your filters at the top of the dashboard
class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"
    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector",
        ),
        ReportDropdown(id="selector", name="user-selection"),
    ]


# The whole report page, stitched together
class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


# App setup – like flipping the switch to turn things on
app = FastHTML()
report = Report()


# Default landing page shows report for Employee #1
@app.get("/")
def home():
    return report("1", Employee())


# Endpoint to view individual employee dashboards
@app.get("/employee/{iid:str}")
def employee_report(iid: str):
    return report(iid, Employee())


# Same thing, but for teams
@app.get("/team/{iid:str}")
def team_report(iid: str):
    return report(iid, Team())


# Called when switching between Employee or Team dropdown options
@app.get("/update_dropdown")
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    profile_type = r.query_params["profile_type"]
    return dropdown(None, Team() if profile_type == "Team" else Employee())


# Handles form submission and redirects you to the correct report
@app.post("/update_data")
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict["profile_type"]
    user_id = data._dict["user-selection"]
    return RedirectResponse(f"/{profile_type.lower()}/{user_id}", status_code=303)


# Start the app!
serve()
