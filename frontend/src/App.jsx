import React, { useState, useRef } from "react";
import { analyzeFile } from "./api/api";

import Header from "./components/Header";
import ImageUploadPanel from "./components/ImageUploadPanel";
import ResultsPanel from "./components/ResultsPanel";
import StrategyCard from "./components/StrategyCard";

import { AlertCircle, CheckCircle2, RefreshCcw } from "lucide-react";

export default function App() {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState("image");
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const selectedFile = e.target.files?.[0];

    if (selectedFile) {
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
      setFileType(selectedFile.type.startsWith("video") ? "video" : "image");
      setResult(null);
      setError(null);
    }
  };

  const processFile = async () => {
    if (!file) return;

    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      const backendResponse = await analyzeFile(file);

      console.log("API RESPONSE:", backendResponse);

      if (backendResponse.status !== "success") {
        throw new Error(backendResponse.error || "Backend analysis failed");
      }

      const data = backendResponse.data;
      const mode = backendResponse.mode;

      if (mode === "video") {
        const trackList = Object.entries(data.results || {}).map(
          ([id, track]) => ({ id, ...track })
        );

        setResult({
          mode: "video",
          summaryPath: data.summary_path,
          tracks: trackList,
        });
      } else {
        setResult({
          mode: "image",
          plateNumber: data.plate || "NOT_FOUND",
          state: data.state || "UNKNOWN",
          type: data.nickname || "N/A",
          confidence:
            data.confidence === "VERIFIED_STATE_MATCH"
              ? "HIGH"
              : data.confidence?.includes("HIGH")
              ? "HIGH"
              : data.confidence?.includes("REFINED")
              ? "MEDIUM"
              : "LOW",
          rawText: data.standard_raw || data.standard_cleaned || "",
          detectionUrl: data.annotated_detection_url || null,
        });
      }
    } catch (err) {
      console.error("ANALYSIS ERROR:", err.response?.data || err);

      setError(
        err.response?.data?.error ||
          err.response?.data?.raw ||
          err.message ||
          "Failed to process file. Make sure the backend is running."
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const resetPipeline = () => {
    setPreviewUrl(null);
    setFile(null);
    setFileType("image");
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
              previewUrl={previewUrl}
              fileType={fileType}
              result={result}
              isProcessing={isProcessing}
              fileInputRef={fileInputRef}
              handleFileUpload={handleFileUpload}
              processFile={processFile}
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
              processFile={processFile}
              resetPipeline={resetPipeline}
            />
          </div>
        </div>
      </main>
    </div>
  );
}