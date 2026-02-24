import gradio as gr
import pandas as pd
import tempfile
from pathlib import Path


def datamorph_ui(csv_file):
    try:
        # Read uploaded CSV
        df = pd.read_csv(csv_file.name)

        # Clean data
        df = df.fillna("N/A")
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        # Parse date columns
        for col in df.columns:
            if "date" in col:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # Save to a temporary Excel file
        tmp_dir = tempfile.mkdtemp()
        output_path = Path(tmp_dir) / "datamorph_report.xlsx"
        df.to_excel(output_path, index=False, engine="openpyxl")

        return str(output_path), "✅ Conversion successful! Download your Excel file below."

    except Exception as e:
        return None, f"❌ Error: {e}"


with gr.Blocks(title="DataMorph — CSV to Excel Converter") as demo:
    gr.Markdown("# 🧬 DataMorph")
    gr.Markdown("Upload a CSV file and convert it into a clean Excel report (.xlsx).")

    with gr.Row():
        csv_input = gr.File(label="Upload CSV file", file_types=[".csv"])

    convert_btn = gr.Button("Convert to Excel")

    excel_output = gr.File(label="Download Excel Report")
    status = gr.Textbox(label="Status", interactive=False)

    convert_btn.click(
        fn=datamorph_ui,
        inputs=csv_input,
        outputs=[excel_output, status]
    )

if __name__ == "__main__":
    demo.launch()