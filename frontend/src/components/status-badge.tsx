type Status = "success" | "failed" | "running";

const statusMap: Record<Status, string> = {
  success: "bg-green-500/20 text-green-400",
  failed: "bg-red-500/20 text-red-400",
  running: "bg-yellow-500/20 text-yellow-400",
};

export default function StatusBadge({ status }: { status: Status }) {
  return (
    <span
      className={`px-3 py-1 rounded-full text-sm font-medium ${statusMap[status]}`}
    >
      {status.toUpperCase()}
    </span>
  );
}
