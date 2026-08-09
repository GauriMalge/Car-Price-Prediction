import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Visualization import generate_plots
from ML import predict_car_price
from Gradio.gradio import gradio

from function import (
    clean_and_prepare_data,
    load_data,
    process_features,
    
)


def main():
    # 1. Pipeline execution to prepare the training data
    data_path = PROJECT_ROOT / "data" / "imports-85.data"
    df_raw = load_data(data_path)
    df_clean = clean_and_prepare_data(df_raw)
    df_processed = process_features(df_clean)

    # 2. Train the Regression Model and extract charts
    
    fig1, fig2, fig3, fig4, fig5 = generate_plots(df_processed)

    # 3. Define the Prediction Logic function
    predict_car_price


    # 4. Construct the Dashboard Layout using Blocks
    gradio(df_processed, fig1, fig2, fig3, fig4, fig5)



if __name__ == "__main__":
    main()
