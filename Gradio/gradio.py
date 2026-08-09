
import gradio as gr
from src.ML import predict_car_price


def gradio(df_processed, fig1, fig2, fig3, fig4, fig5):
    with gr.Blocks(theme="soft") as app:
        gr.Markdown("Automobile Machine Learning & Analytics Dashboard")
        gr.Markdown("Explore the dataset insights or use the predictive model to calculate current valuations.")

        with gr.Tab("🔮 Price Predictor"):
            gr.Markdown("### Enter Automobile Specifications:")
            with gr.Row():
                with gr.Column():
                    hp = gr.Slider(minimum=40, maximum=300, value=100, label="Horsepower (hp)", step=1)
                    eng_size = gr.Slider(minimum=60, maximum=350, value=120, label="Engine Size (cu in)", step=1)
                    weight = gr.Slider(minimum=1400, maximum=4100, value=2500, label="Curb Weight (lbs)", step=10)
                    mpg = gr.Slider(minimum=10, maximum=60, value=25, label="City MPG", step=1)
                    fuel = gr.Dropdown(choices=["Gas", "Diesel"], value="Gas", label="Fuel Type")
                    submit_btn = gr.Button("Calculate Price", variant="primary")
                
                with gr.Column():
                    gr.Markdown("### Valuation Analysis Engine Output")
                    output_text = gr.Textbox(label="Model Output Calculation", placeholder="Results will appear here...")
            
            # Map button trigger to the prediction logic
            submit_btn.click(
                fn=predict_car_price, 
                inputs=[hp, eng_size, weight, mpg, fuel, df_processed], 
                outputs=output_text
            )

        with gr.Tab("📊 Data Analysis & Visualizations"):
            gr.Markdown("### Exploratory Data Plots Generated from the Dataset Pipeline")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Horsepower Distribution")
                    gr.Plot(value=fig1)
                with gr.Column():
                    gr.Markdown("#### Binned Horsepower vs Price")
                    gr.Plot(value=fig2)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Price vs Fuel Consumption (L/100km)")
                    gr.Plot(value=fig3)
                with gr.Column():
                    gr.Markdown("#### Vehicle Body Style Distribution")
                    gr.Plot(value=fig4)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Body Style Market Pricing segmented by Fuel Strategy")
                    gr.Plot(value=fig5)

    # 5. Launch web application interface
    app.launch(theme="soft")