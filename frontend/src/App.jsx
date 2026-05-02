import React, { useState, useRef } from "react";
import { analyzePlate } from "./api/api";

import Header from "./components/Header";
import ImageUploadPanel from "./components/ImageUploadPanel";
import ResultsPanel from "./components/ResultsPanel";
import StrategyCard from "./components/StrategyCard";

import { AlertCircle, CheckCircle2, RefreshCcw } from "lucide-react";

export default function App() {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const selectedFile = e.target.files?.[0];

    if (selectedFile) {
      setFile(selectedFile);
      setImage(URL.createObjectURL(selectedFile));
      setResult(null);
      setError(null);
    }
  };

  const processImage = async () => {
    if (!file) return;

    setIsProcessing(true);
    setError(null);

    try {
      const backendResponse = await analyzePlate(file);

      if (backendResponse.status !== "success") {
        throw new Error(backendResponse.error || "Backend analysis failed");
      }

      const data = backendResponse.data;

      setResult({
        plateNumber: data.plate,
        state: data.state,
        type: data.nickname || "Standard",
        confidence:
          data.confidence === "VERIFIED_STATE_MATCH"
            ? "HIGH"
            : data.confidence?.includes("HIGH")
            ? "HIGH"
            : data.confidence?.includes("REFINED")
            ? "MEDIUM"
            : "LOW",
        rawText: data.standard_raw,
        detectionUrl: data.annotated_detection_url,
      });
    } catch (err) {
      setError(
        err.message || "Failed to process image. Make sure the backend is running."
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const resetPipeline = () => {
    setImage(null);
    setFile(null);
    setResult(null);
    setError(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-12 gap-8">
          <div className="lg:col-span-7 space-y-6">
            <ImageUploadPanel
              image={image}
              result={result}
              isProcessing={isProcessing}
              fileInputRef={fileInputRef}
              handleFileUpload={handleFileUpload}
              processImage={processImage}
            />

            <section className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6">
              <h3 className="font-display font-semibold text-slate-800 mb-6 flex items-center gap-2">
                <RefreshCcw className="w-5 h-5 text-slate-400" />
                Pipeline Strategy Recommendations
              </h3>

              <div className="grid md:grid-cols-2 gap-4">
                <StrategyCard
                  title="Format-Aware Correction"
                  description="Use regex and plate rules to reduce OCR errors like 0/O, 1/I, and 5/S."
                  icon={<AlertCircle className="w-5 h-5 text-orange-500" />}
                />

                <StrategyCard
                  title="State Mapping"
                  description="Verify plate prefix and state metadata using Nigerian plate rules."
                  icon={<CheckCircle2 className="w-5 h-5 text-green-500" />}
                />
              </div>
            </section>
          </div>

          <div className="lg:col-span-5">
            <ResultsPanel
              result={result}
              error={error}
              processImage={processImage}
              resetPipeline={resetPipeline}
            />
          </div>
        </div>
      </main>
    </div>
  );
}