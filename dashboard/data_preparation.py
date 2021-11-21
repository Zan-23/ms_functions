import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# see https://plotly.com/python/px-arguments/ for more options


def generate_figures(colors):
    main_df = pd.read_csv("test_data.csv", sep=";")
    main_df["datetime"] = pd.to_datetime(main_df["datetime"])

    # scratches_fig = go.Figure(
    #     go.Scattergl(
    #         x=main_df["datetime"],
    #         y=main_df["has_scratch"],
    #         mode='markers+lines',
    #     )
    # )
    # scratches_fig.update_layout(
    #     # paper_bgcolor=colors['background'],
    #     # font_color=colors['text'],
    #     height=300
    # )
    scratches_fig = px.scatter(x=main_df["datetime"], y=main_df["has_scratch"],
                               template="plotly_dark")
    scratches_fig.data[0].update(mode='markers+lines')
    scratches_fig.update_traces(line_color='#a2fca2', marker_color='#a2fca2')
    scratches_fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Defected image yes/no",
        height=300
    )

    return scratches_fig

# fig = px.bar(main_df, x="datetime", y="Amount", color="City", barmode="stack")
#
# fig.update_layout(
#     font_color=colors['text'],
#     height=300
# )
