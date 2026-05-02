import { Database } from "lucide-react";

export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="bg-nigeria-green p-1.5 rounded-lg">
            <Database className="w-5 h-5 text-white" />
          </div>

          <h1 className="font-display font-extrabold text-xl tracking-tight text-slate-800">
            NAIJAPLATE <span className="text-nigeria-green">AI</span>
          </h1>
        </div>

        <div className="flex items-center gap-4 text-xs font-medium text-slate-500 uppercase tracking-widest">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 bg-nigeria-green rounded-full animate-pulse" />
            Pipeline Active
          </span>
        </div>
      </div>
    </header>
  );
}