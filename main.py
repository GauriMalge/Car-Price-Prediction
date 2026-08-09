import os
import sys
import gradio as gr
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.api import app as fastapi_app
from src.function import load_data, clean_and_prepare_data, process_features
from src.Visualization import generate_plots

# Configuration from environment variables (for Azure)
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("WEBSITE_HOSTNAME", "127.0.0.1") if os.getenv("WEBSITE_HOSTNAME") else "0.0.0.0"

# Load data and plots at startup
PROJECT_ROOT = Path(__file__).resolve().parent
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
    """Call the FastAPI backend directly"""
    try:
        from src.ML import predict_car_price
        result = predict_car_price(
            horsepower,
            engine_size,
            curb_weight,
            city_mpg,
            fuel_type,
            None  # Will use model from module
        )
        return f"${result:,.2f}"
    except Exception as e:
        return f"Prediction error: {e}"


def build_gradio_interface():
    """Build Gradio interface"""
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
                fn=predict_via_api,
                inputs=[horsepower, engine_size, curb_weight, city_mpg, fuel_type],
                outputs=output
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

    return demo


# Mount Gradio app inside FastAPI
demo = build_gradio_interface()
app = gr.mount_gradio_app(fastapi_app, demo, path="/")


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Starting Car Price Predictor (Single Process)")
    print(f"📍 Server running on http://{HOST}:{PORT}")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )
