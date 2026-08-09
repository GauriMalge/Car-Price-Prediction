import gradio as gr
import requests
from function import load_data, clean_and_prepare_data, process_features
from Visualization import generate_plots
from pathlib import Path

API_URL = "http://127.0.0.1:8000/predict"

# Load data and plots at startup
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "imports-85.data"

try:
    df_raw = load_data(DATA_PATH)
    df_clean = clean_and_prepare_data(df_raw)
    df_processed = process_features(df_clean)
    plots = generate_plots(df_processed)
except Exception as e:
    plots = None
    print(f"Error loading plots: {e}")


def predict_via_api(horsepower, engine_size, curb_weight, city_mpg, fuel_type):
    try:
        payload = {
            "horsepower": horsepower,
            "engine_size": engine_size,
            "curb_weight": curb_weight,
            "city_mpg": city_mpg,
            "fuel_type": fuel_type
        }
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status()
        return response.json().get("prediction", "No prediction returned")
    except Exception as e:
        return f"API error: {e}"


with gr.Blocks() as demo:
    gr.Markdown("Car Price Predictor")

    with gr.Tab("🔮 Price Predictor"):
        horsepower = gr.Slider(40, 300, value=100, label="Horsepower")
        engine_size = gr.Slider(60, 350, value=120, label="Engine Size")
        curb_weight = gr.Slider(1400, 4100, value=2500, label="Curb Weight")
        city_mpg = gr.Slider(10, 60, value=25, label="City MPG")
        fuel_type = gr.Dropdown(["Gas", "Diesel"], value="Gas", label="Fuel Type")
        output = gr.Textbox(label="Result")
        btn = gr.Button("Predict")
        btn.click(fn=predict_via_api, inputs=[horsepower, engine_size, curb_weight, city_mpg, fuel_type], outputs=output)

    with gr.Tab("📊 Analytics"):
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
            gr.Markdown("⚠️ Could not load visualization charts. Check data file and backend.")


