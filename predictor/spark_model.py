import os
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel
from pyspark.sql.types import StructType, StructField, DoubleType

# ============================================================
# GLOBAL SINGLETONS (KHÔNG KHỞI TẠO NGAY)
# ============================================================
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

_spark = None
_model = None

# ============================================================
# PATH CONFIG
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "spark_logistic_cardio_model"
)

# ============================================================
# INPUT DATA SCHEMA (GIỮ NGUYÊN)
# ============================================================

input_schema = StructType([
    StructField("age", DoubleType(), True),
    StructField("gender", DoubleType(), True),
    StructField("height", DoubleType(), True),
    StructField("weight", DoubleType(), True),
    StructField("ap_hi", DoubleType(), True),
    StructField("ap_lo", DoubleType(), True),
    StructField("cholesterol", DoubleType(), True),
    StructField("gluc", DoubleType(), True),
    StructField("smoke", DoubleType(), True),
    StructField("alco", DoubleType(), True),
    StructField("active", DoubleType(), True),
])

# ============================================================
# SPARK INITIALIZER (LAZY)
# ============================================================

def get_spark():
    global _spark
    if _spark is None:
        _spark = (
            SparkSession.builder
            .appName("HeartDiseasePredictionWeb")
            .master("local[*]")
            .getOrCreate()
        )
    return _spark

# ============================================================
# MODEL LOADER (LAZY)
# ============================================================

def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Spark model not found at: {MODEL_PATH}"
            )
        spark = get_spark()
        _model = PipelineModel.load(MODEL_PATH)
    return _model

# ============================================================
# PREDICTION FUNCTION (GIỮ NGUYÊN LOGIC)
# ============================================================

def predict_heart_disease(input_data: dict):
    spark = get_spark()
    model = get_model()

    # ÉP KIỂU TẤT CẢ GIÁ TRỊ SANG FLOAT
    cleaned_data = {
        k: float(v) if v is not None else None
        for k, v in input_data.items()
    }

    df = spark.createDataFrame(
        [cleaned_data],
        schema=input_schema
    )

    result = (
        model.transform(df)
        .select("prediction", "probability")
        .collect()[0]
    )

    return {
        "prediction": int(result["prediction"]),
        "probability": float(result["probability"][1])
    }
