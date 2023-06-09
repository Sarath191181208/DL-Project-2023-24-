import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib import patches

from typing import Any, Generator, Tuple, Union


def generate_color():
    pastel_colors = ['#FB9389', '#B3CDE3', '#CCEBC5', '#DECBE4', '#FED9A6', '#FFFFCC']
    pastel_index = 0
    
    while True:
        yield pastel_colors[pastel_index % len(pastel_colors)]
        pastel_index += 1

def get_rect_center(rect) -> Tuple[float, float]:
    x = rect.get_x() + rect.get_width() / 2
    y = rect.get_y() + rect.get_height() / 2
    return (x, y)

def square_area_proportion_plot(percentage_percentile_df: pd.DataFrame, ax: Union[plt.Axes, None] = None) -> None:
    max_val = percentage_percentile_df['percentage'].max()

    _, ax = plt.subplots(figsize=(max_val*15, 3*max_val*5)) if ax is None else (None, ax)
    # fig, ax = plt.subplots(figsize=(15, 15))
    colors_gen = generate_color()
    ax.xaxis.set_visible(False); ax.yaxis.set_visible(False)
    ax.axis('off')

    # dictionary to keep track which color is used for which percentile
    colors_dict = {}
    def generate_and_save_color(row: Union[pd.Series, pd.DataFrame]):
        generated_color = next(colors_gen)
        row_name = row['percentile'].values[0] if isinstance(row, pd.DataFrame) else row['percentile']
        colors_dict[row_name] = generated_color
        return generated_color

    def draw_patch( x: float, y: float, width: float, height: float, color: str, value: float):
        rect = patches.Rectangle((x, y), width, height, color=color, alpha=0.8)
        cx, cy = get_rect_center(rect)
        ax.annotate(f'{value:.2f}', (cx, cy), color='black', fontsize=12, ha='center', va='center')
        ax.add_patch( rect )

    # sort the data by percentage
    percentage_percentile_df = percentage_percentile_df.sort_values(by=['percentage'])
    # get the whole row with the max percentage
    max_val = percentage_percentile_df['percentage'].max()
    max_val_row = percentage_percentile_df[percentage_percentile_df['percentage'] == max_val]

    if max_val < 0.5:
        # draw the max_value sq in the left side 
        generated_color = generate_and_save_color(max_val_row)
        draw_patch(0, 0, max_val, max_val, color=generated_color, value=max_val)
        # remove the max value from the dataframe
        percentage_percentile_df = percentage_percentile_df[percentage_percentile_df['percentage'] != max_val]
        min_val = percentage_percentile_df['percentage'].min()
        min_val_row = percentage_percentile_df[percentage_percentile_df['percentage'] == min_val]
        # draw the min_value sq in the left side
        min_val_height = (min_val / max_val) * max_val
        generated_color = generate_and_save_color(min_val_row)
        # save the color in a dict
        draw_patch(0, max_val, max_val,min_val_height, color= generated_color, value=min_val ) 
        # remove the min value from the dataframe
        percentage_percentile_df = percentage_percentile_df[percentage_percentile_df['percentage'] != min_val]
        drawn_height = max_val + min_val_height

    else:
        # draw the max_value sq in the left side 
        generated_color = generate_and_save_color(max_val_row)
        draw_patch(0, 0, max_val, max_val, color=generated_color, value=max_val )
        # remove the max value from the dataframe
        percentage_percentile_df = percentage_percentile_df[percentage_percentile_df['percentage'] != max_val]
        drawn_height = max_val
    remaining_width = min(1 - max_val, max_val)
    sum_vals = percentage_percentile_df['percentage'].sum()
    running_height_sum = 0
    # draw the remaining sq in the right side
    for i, row in percentage_percentile_df.iterrows():
        height = (row['percentage'] / sum_vals) * drawn_height
        generated_color = generate_and_save_color(row)
        draw_patch(max_val, running_height_sum, remaining_width, height, color=generated_color, value=row['percentage']) 
        running_height_sum += height

    # draw the legend
    legend = []
    for key, value in colors_dict.items():
        legend.append( patches.Patch(color=value, label=key) )
    ax.legend(handles=legend)
    
if __name__ == "__main__":
    test_df = pd.DataFrame({
        'percentile': ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60'], 
        'percentage': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    })
    square_area_proportion_plot(test_df)