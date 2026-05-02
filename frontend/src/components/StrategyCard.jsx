export default function StrategyCard({ title, description, icon }) {
  return (
    <div className="p-4 rounded-2xl border border-slate-100 bg-slate-50 flex gap-4 items-start">
      <div className="mt-1">{icon}</div>

      <div>
        <h4 className="font-semibold text-slate-800 text-sm">{title}</h4>
        <p className="text-xs text-slate-500 mt-1 leading-relaxed">
          {description}
        </p>
      </div>
    </div>
  );
}