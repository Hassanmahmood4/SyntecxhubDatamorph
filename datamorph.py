import argparse
import pandas as pd
import logging
from pathlib import Path

# ---------------- Logging Setup ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ---------------- Core Logic ----------------
def datamorph(input_file: Path, output_file: Path):
    try:
        logging.info(f"📥 Loading CSV: {input_file}")
        df = pd.read_csv(input_file)

        logging.info("🧹 Cleaning data...")

        # Fill missing values
        df = df.fillna("N/A")

        # Normalize column names
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        # Parse date-like columns
        for col in df.columns:
            if "date" in col:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        logging.info(f"📤 Exporting to Excel: {output_file}")
        df.to_excel(output_file, index=False, engine="openpyxl")

        logging.info("✅ DataMorph completed successfully!")

    except FileNotFoundError:
        logging.error("❌ Input file not found.")
    except pd.errors.EmptyDataError:
        logging.error("❌ CSV file is empty.")
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")

# ---------------- CLI ----------------
def main():
    parser = argparse.ArgumentParser(
        description="🧬 DataMorph — Clean & Convert CSV to Excel"
    )
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", required=True, help="Path to output Excel (.xlsx) file")

    args = parser.parse_args()

    datamorph(Path(args.input), Path(args.output))

if __name__ == "__main__":
    main()