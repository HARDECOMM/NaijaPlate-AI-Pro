export const ENV = {
  PORT: process.env.PORT || 5000,

  ML_SERVICE_URL:
    process.env.ML_SERVICE_URL ||
    "http://127.0.0.1:7860",
};