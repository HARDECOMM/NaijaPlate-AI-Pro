import { Camera, Upload, Search, Zap } from "lucide-react";

export default function ImageUploadPanel({
  previewUrl,
  fileType,
  result,
  isProcessing,
  fileInputRef,
  handleFileUpload,
  processFile,
}) {
  return (
    <section className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
      <div className="p-6 border-b border-slate-100 flex items-center justify-between">
        <div>
          <h2 className="font-display font-semibold text-lg">Input Analysis</h2>
          <p className="text-sm text-slate-500">
            Upload a license plate image for AI refinement
          </p>
        </div>

        <button
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl transition-colors font-medium text-sm"
        >
          <Upload className="w-4 h-4" />
          Select Image or Video
        </button>

        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          accept="image/*,video/*"
          onChange={handleFileUpload}
        />
      </div>

      <div className="p-8 aspect-video relative flex items-center justify-center bg-slate-100/50">
        {previewUrl ? (
          <div className="relative group w-full h-full">
            {fileType === "video" ? (
              <video
                src={previewUrl}
                className="w-full h-full object-contain rounded-xl shadow-lg"
                controls
              />
            ) : (
              <img
                src={previewUrl}
                className="w-full h-full object-contain rounded-xl shadow-lg transition-opacity duration-300"
                alt="Plate preview"
              />
            )}

            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors pointer-events-none rounded-xl" />

            {result && (
              <div className="absolute top-4 right-4 bg-nigeria-green text-white text-[10px] font-bold px-2 py-1 rounded shadow-sm">
                ANALYZED
              </div>
            )}
          </div>
        ) : (
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-white rounded-2xl shadow-sm border border-slate-200 flex items-center justify-center mx-auto text-slate-400">
              <Camera className="w-8 h-8" />
            </div>

            <p className="text-slate-400 font-medium">No file selected</p>
          </div>
        )}

        {isProcessing && (
          <div className="absolute inset-0 bg-white/80 backdrop-blur-sm flex flex-col items-center justify-center space-y-4 z-10">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-slate-100 border-t-nigeria-green rounded-full animate-spin" />
              <Zap className="w-6 h-6 text-nigeria-green absolute inset-0 m-auto animate-pulse" />
            </div>

            <div className="text-center">
              <p className="font-display font-bold text-slate-800">
                GEMINI REFINING...
              </p>
              <p className="text-xs text-slate-500 uppercase tracking-widest mt-1">
                Applying format-aware OCR
              </p>
            </div>
          </div>
        )}
      </div>

      <div className="p-6 bg-slate-50 flex justify-end gap-3">
        <button
          disabled={!previewUrl || isProcessing}
          onClick={processFile}
          className="px-6 py-3 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg flex items-center gap-2"
        >
          <Search className="w-5 h-5" />
          Run Diagnostic
        </button>
      </div>
    </section>
  );
}