import json
import os
import pandas as pd

RAW_FILE = "data/raw/breeds_raw.json"

PROCESSED_FOLDER = "data/processed"

REGRESSION_FILE = f"{PROCESSED_FOLDER}/regression_data.json"
LOGISTIC_FILE = f"{PROCESSED_FOLDER}/logistic_data.json"
CLASSIFICATION_FILE = f"{PROCESSED_FOLDER}/classification_data.json"


def load_raw():
    with open(RAW_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_data():
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    raw_data = load_raw()

    breeds = raw_data["data"]

    transformed = []

    for breed in breeds:
        attr = breed["attributes"]

        try:
            life_min = attr["life"]["min"]
            life_max = attr["life"]["max"]

            male_weight_min = attr["male_weight"]["min"]
            male_weight_max = attr["male_weight"]["max"]

            female_weight_min = attr["female_weight"]["min"]
            female_weight_max = attr["female_weight"]["max"]

            hypoallergenic = 1 if attr["hypoallergenic"] else 0

            avg_life = (life_min + life_max) / 2
            avg_male_weight = (male_weight_min + male_weight_max) / 2
            avg_female_weight = (female_weight_min + female_weight_max) / 2

            # VARIABLE OBJETIVO BINARIA
            # 1 = perro grande
            # 0 = perro pequeño
            is_large = 1 if avg_male_weight >= 25 else 0

            transformed.append({

                "name": attr["name"],

                # TARGET
                "avg_life": avg_life,

                # FEATURES
                "life_min": life_min,
                "life_max": life_max,

                "avg_male_weight": avg_male_weight,
                "avg_female_weight": avg_female_weight,

                "male_weight_min": male_weight_min,
                "male_weight_max": male_weight_max,

                "female_weight_min": female_weight_min,
                "female_weight_max": female_weight_max,

                "weight_difference": abs(
                    avg_male_weight - avg_female_weight
                ),

                "hypoallergenic": hypoallergenic,

                # CLASIFICACIÓN
                "is_large": is_large
            })
        except:
            continue

    df = pd.DataFrame(transformed)

    # =========================
    # REGRESIÓN
    # predecir expectativa de vida
    # =========================

    regression_df = df[[
        "avg_life",

        "life_min",
        "life_max",

        "avg_male_weight",
        "avg_female_weight",

        "male_weight_min",
        "male_weight_max",

        "female_weight_min",
        "female_weight_max",

        "weight_difference",

        "hypoallergenic"
    ]]

    regression_df.to_json(
        REGRESSION_FILE,
        orient="records",
        indent=4
    )

    # =========================
    # REGRESIÓN LOGÍSTICA
    # 1 o 0
    # =========================

    logistic_df = df[[
        "avg_male_weight",
        "avg_female_weight",
        "hypoallergenic",
        "is_large"
    ]]

    logistic_df.to_json(
        LOGISTIC_FILE,
        orient="records",
        indent=4
    )

    # =========================
    # ÁRBOL CLASIFICACIÓN
    # =========================

    classification_df = logistic_df.copy()

    classification_df.to_json(
        CLASSIFICATION_FILE,
        orient="records",
        indent=4
    )

    print("Transformación completada")
    print(f"Archivo regresión: {REGRESSION_FILE}")
    print(f"Archivo logística: {LOGISTIC_FILE}")
    print(f"Archivo clasificación: {CLASSIFICATION_FILE}")


if __name__ == "__main__":
    transform_data()