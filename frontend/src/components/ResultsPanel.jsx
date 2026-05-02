import { motion, AnimatePresence } from "framer-motion";
import { AlertCircle, CheckCircle2, ChevronRight } from "lucide-react";
import { validateNigerianPlate } from "../lib/plate-utils";

export default function ResultsPanel({
  result,
  error,
  processImage,
  resetPipeline,
}) {
  return (
    <AnimatePresence mode="wait">
      {result ? (
        <motion.div
          key="result"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="space-y-6"
        >
          <div className="bg-white rounded-3xl border-2 border-slate-200 shadow-xl overflow-hidden">
            <div className="bg-slate-900 p-6 text-white text-center">
              <p className="text-xs font-medium text-white/50 uppercase tracking-[0.2em] mb-2">
                Extracted Number
              </p>

              <div className="text-5xl font-mono font-bold tracking-tighter text-blue-400">
                {result.plateNumber}
              </div>
            </div>

            <div className="p-6 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <p className="text-xs text-slate-400 uppercase font-bold tracking-wider">
                    Identified State
                  </p>
                  <p className="text-lg font-display font-bold text-slate-800">
                    {result.state}
                  </p>
                </div>

                <div className="space-y-1 text-right">
                  <p className="text-xs text-slate-400 uppercase font-bold tracking-wider">
                    State Slogan
                  </p>

                  <span className="px-3 py-1 rounded-full text-xs font-bold bg-blue-50 text-blue-600 border border-blue-100">
                    {result.type}
                  </span>
                </div>
              </div>

              <div className="pt-6 border-t border-slate-100 space-y-4">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-slate-600">
                    Verification Confidence
                  </p>

                  <div className="flex items-center gap-1.5">
                    <span
                      className={`w-2 h-2 rounded-full ${
                        result.confidence === "HIGH"
                          ? "bg-green-500"
                          : result.confidence === "MEDIUM"
                          ? "bg-orange-500"
                          : "bg-red-500"
                      }`}
                    />

                    <span className="font-bold text-slate-800">
                      {result.confidence}
                    </span>
                  </div>
                </div>

                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{
                      width:
                        result.confidence === "HIGH"
                          ? "95%"
                          : result.confidence === "MEDIUM"
                          ? "60%"
                          : "30%",
                    }}
                    className={`h-full ${
                      result.confidence === "HIGH"
                        ? "bg-green-500"
                        : result.confidence === "MEDIUM"
                        ? "bg-orange-500"
                        : "bg-red-500"
                    }`}
                  />
                </div>
              </div>

              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-slate-400">
                  <span>PIPELINE VALIDATION</span>

                  {validateNigerianPlate(result.plateNumber) ? (
                    <span className="text-green-600 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      FORMAT VALID
                    </span>
                  ) : (
                    <span className="text-red-500 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" />
                      INVALID FORMAT
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>

          <button
            onClick={resetPipeline}
            className="w-full py-4 rounded-2xl border border-slate-200 text-slate-500 font-medium hover:bg-slate-100 transition-colors"
          >
            Reset Pipeline
          </button>
        </motion.div>
      ) : error ? (
        <motion.div
          key="error"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-red-50 border border-red-100 p-6 rounded-3xl text-center space-y-4"
        >
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto" />

          <div>
            <h4 className="font-display font-bold text-red-900">
              Analysis Failed
            </h4>
            <p className="text-sm text-red-600 mt-1">{error}</p>
          </div>

          <button
            onClick={processImage}
            className="px-4 py-2 bg-red-600 text-white rounded-xl font-medium text-sm hover:bg-red-700 transition-colors"
          >
            Retry Analysis
          </button>
        </motion.div>
      ) : (
        <div className="bg-white rounded-3xl border border-slate-200 border-dashed p-12 text-center space-y-4">
          <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto text-slate-300">
            <ChevronRight className="w-8 h-8" />
          </div>

          <div>
            <p className="text-slate-500 font-medium">Diagnostic Results</p>
            <p className="text-xs text-slate-400 mt-1">
              Real-time analysis will appear here
            </p>
          </div>
        </div>
      )}
    </AnimatePresence>
  );
}