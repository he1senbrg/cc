from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pred_level
import pred_quality
import json
import ai_report
import dataset
import os
import shutil
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    dir_path = "static"
    shutil.rmtree(dir_path, ignore_errors=True)
    os.makedirs(dir_path, exist_ok=True)
    print(f"Reset directory: {dir_path}")

    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://aigis.vishnu.studio",
    "https://nice-ocean-03325dd00.3.azurestaticapps.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"Info": "AIGIS API"}


@app.post("/analyze")
def analyze_data(data: dict):
    quality_input = {
        "pH": float(data.get("ph", 0.0) or 0.0),
        "EC": float(data.get("ec", 0) or 0),
        "TDS": float(data.get("tds", 0) or 0),
        "TH": float(data.get("th", 0) or 0),
        "Ca": float(data.get("ca", 0) or 0),
        "Mg": float(data.get("mg", 0) or 0),
        "Na": float(data.get("na", 0) or 0),
        "K": float(data.get("k", 0) or 0),
        "Cl": float(data.get("cl", 0) or 0),
        "SO4": float(data.get("so4", 0) or 0),
        "NO3": float(data.get("nitrate", 0) or 0),
        "F": float(data.get("fluoride", 0.0) or 0.0),
        "U(ppb)": float(data.get("uranium", 0) or 0),
    }

    quality_analysis = pred_quality.predict(quality_input)

    level_input = [
        float(data.get("annualDomesticIndustryDraft", 0.0) or 0.0),
        float(data.get("annualIrrigationDraft", 0.0) or 0.0),
        float(data.get("annualGroundwaterDraftTotal", 0.0) or 0.0),
        float(data.get("annualReplenishableGroundwaterResources", 0.0) or 0.0),
        float(data.get("naturalDischargeNonMonsoon", 0.0) or 0.0),
        float(data.get("netGroundwaterAvailability", 0.0) or 0.0),
    ]

    level_analysis = pred_level.predict(level_input)

    retJSON = {"quality_analysis": quality_analysis, "level_analysis": level_analysis}
    print("Analysis result:", retJSON)
    return json.dumps(retJSON)


@app.post("/predict")
def predict_data(data: dict):
    existing = data.get("existing", {})

    quality_existing = {
        "pH": float(existing.get("ph", 0.0) or 0.0),
        "EC": float(existing.get("ec", 0) or 0),
        "TDS": float(existing.get("tds", 0) or 0),
        "TH": float(existing.get("th", 0) or 0),
        "Ca": float(existing.get("ca", 0) or 0),
        "Mg": float(existing.get("mg", 0) or 0),
        "Na": float(existing.get("na", 0) or 0),
        "K": float(existing.get("k", 0) or 0),
        "Cl": float(existing.get("cl", 0) or 0),
        "SO4": float(existing.get("so4", 0) or 0),
        "NO3": float(existing.get("nitrate", 0) or 0),
        "F": float(existing.get("fluoride", 0.0) or 0.0),
        "U(ppb)": float(existing.get("uranium", 0) or 0),
    }

    level_existing = [
        float(existing.get("annualDomesticIndustryDraft", 0.0) or 0.0),
        float(existing.get("annualIrrigationDraft", 0.0) or 0.0),
        float(existing.get("annualGroundwaterDraftTotal", 0.0) or 0.0),
        float(existing.get("annualReplenishableGroundwaterResources", 0.0) or 0.0),
        float(existing.get("naturalDischargeNonMonsoon", 0.0) or 0.0),
        float(existing.get("netGroundwaterAvailability", 0.0) or 0.0),
    ]

    for_prediction = data.get("for_prediction", {})

    quality_for_prediction = {
        "pH": float(for_prediction.get("ph", 0.0) or 0.0),
        "EC": int(for_prediction.get("ec", 0) or 0),
        "TDS": int(for_prediction.get("tds", 0) or 0),
        "TH": int(for_prediction.get("th", 0) or 0),
        "Ca": int(for_prediction.get("ca", 0) or 0),
        "Mg": int(for_prediction.get("mg", 0) or 0),
        "Na": int(for_prediction.get("na", 0) or 0),
        "K": int(for_prediction.get("k", 0) or 0),
        "Cl": int(for_prediction.get("cl", 0) or 0),
        "SO4": int(for_prediction.get("so4", 0) or 0),
        "NO3": int(for_prediction.get("nitrate", 0) or 0),
        "F": float(for_prediction.get("fluoride", 0.0) or 0.0),
        "U(ppb)": int(for_prediction.get("uranium", 0) or 0),
    }

    level_for_prediction_parameters = for_prediction.get("groundwaterParameters", {})

    level_for_prediction_parameters = {
        i["type"]: i["value"] for i in level_for_prediction_parameters
    }

    level_for_prediction = [
        float(
            level_for_prediction_parameters.get("annualDomesticIndustryDraft", 0.0)
            or 0.0
        ),
        float(level_for_prediction_parameters.get("annualIrrigationDraft", 0.0) or 0.0),
        float(
            level_for_prediction_parameters.get("annualGroundwaterDraftTotal", 0.0)
            or 0.0
        ),
        float(
            level_for_prediction_parameters.get(
                "annualReplenishableGroundwaterResources", 0.0
            )
            or 0.0
        ),
        float(
            level_for_prediction_parameters.get("naturalDischargeNonMonsoon", 0.0)
            or 0.0
        ),
        float(
            level_for_prediction_parameters.get("netGroundwaterAvailability", 0.0)
            or 0.0
        ),
    ]

    quality_input = quality_existing

    level_input = [
        level_existing[i] + level_for_prediction[i] for i in range(len(level_existing))
    ]

    quality_analysis = pred_quality.predict(quality_input)
    level_analysis = pred_level.predict(level_input)

    retJSON = {"quality_analysis": quality_analysis, "level_analysis": level_analysis}
    print("Analysis result:", json.dumps(retJSON, indent=2))
    return json.dumps(retJSON)


@app.post("/gen_report")
def generate_report(data: dict):
    pdf_url = ai_report.generate(data)

    return pdf_url

@app.post("/get_dataset")
def download_dataset(data: dict):
    dataset_url = dataset.download_dataset(data)

    return dataset_url