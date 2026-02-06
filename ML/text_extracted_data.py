import pandas as pd
from text_extractor import extract_from_text


INPUT_FILE = "data/synthetic_village_water_data.csv"
OUTPUT_FILE = "data/synthetic_with_text_features.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    extracted_rows = df["report_text"].apply(extract_from_text)

    extracted_df = pd.DataFrame(list(extracted_rows))

    final_df = pd.concat([df, extracted_df], axis=1)

    final_df.to_csv(OUTPUT_FILE, index=False)

    print("Saved:", OUTPUT_FILE)
    print(final_df.head())


if __name__ == "__main__":
    main()
