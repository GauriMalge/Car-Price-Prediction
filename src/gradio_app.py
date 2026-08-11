import gradio as gr
from pathlib import Path

from function import load_data, clean_and_prepare_data, process_features
from ML import predict_car_price
from Visualization import generate_plots

# Load data and plots at startup
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "imports-85.data"

try:
    df_raw = load_data(DATA_PATH)
    df_clean = clean_and_prepare_data(df_raw)
    df_processed = process_features(df_clean)
    plots = generate_plots(df_processed)
except Exception as e:
    df_processed = None
    plots = None
    print(f"Error loading plots: {e}")


def predict_price(horsepower, engine_size, curb_weight, city_mpg, fuel_type):
    try:
        return predict_car_price(
            horsepower,
            engine_size,
            curb_weight,
            city_mpg,
            fuel_type,
            df_processed,
        )
    except Exception as e:
        return f"Prediction error: {e}"


with gr.Blocks() as demo:
    gr.Markdown("# 🚗 Car Price Predictor")
    gr.Markdown("Predict car prices using machine learning")

    with gr.Tab("🔮 Price Predictor"):
        gr.Markdown("### Enter car specifications:")
        with gr.Row():
            horsepower = gr.Slider(40, 300, value=100, label="Horsepower")
            engine_size = gr.Slider(60, 350, value=120, label="Engine Size")
        with gr.Row():
            curb_weight = gr.Slider(1400, 4100, value=2500, label="Curb Weight")
            city_mpg = gr.Slider(10, 60, value=25, label="City MPG")
        fuel_type = gr.Dropdown(["Gas", "Diesel"], value="Gas", label="Fuel Type")
        output = gr.Textbox(label="Predicted Price", interactive=False)
        btn = gr.Button("🎯 Predict Price", variant="primary")
        btn.click(
            fn=predict_price,
            inputs=[horsepower, engine_size, curb_weight, city_mpg, fuel_type],
            outputs=output,
        )

    with gr.Tab("📊 Analytics"):
        gr.Markdown("### Data Visualizations")
        if plots:
            with gr.Row():
                with gr.Column():
                    gr.Plot(plots[0])
                with gr.Column():
                    gr.Plot(plots[1])
            with gr.Row():
                with gr.Column():
                    gr.Plot(plots[2])
                with gr.Column():
                    gr.Plot(plots[3])
            with gr.Row():
                gr.Plot(plots[4])
        else:
            gr.Markdown("⚠️ Could not load visualization charts. Check data file.")


