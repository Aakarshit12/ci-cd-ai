import React from "react";

type PipelineCardProps = {
  name: string;
  status: "success" | "running" | "failed";
};

const statusColors = {
  success: "bg-green-600",
  running: "bg-yellow-500",
  failed: "bg-red-600"
};

const PipelineCard: React.FC<PipelineCardProps> = ({ name, status }) => {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-6 shadow-lg transition-all">
      <div className="flex items-center gap-2 mb-2">
        <span className={`h-3 w-3 rounded-full ${statusColors[status]}`}></span>
        <span className="font-medium text-lg">{name}</span>
      </div>
      <div className="text-xs text-zinc-400">Status: {status}</div>
    </div>
  );
};

export default PipelineCard;
