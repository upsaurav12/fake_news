import { motion } from "framer-motion";
import { ShieldCheck, ShieldX, ShieldQuestion } from "lucide-react";
import { Progress } from "@/components/ui/progress";

interface VerdictCardProps {
  verdict: string;
  credibilityScore: number;
  confidence: number;
}

const VerdictCard = ({ verdict, credibilityScore, confidence }: VerdictCardProps) => {
  const normalized = verdict.toUpperCase();
  const isTrue = normalized.includes("TRUE") && !normalized.includes("UN");
  const isFalse = normalized.includes("FALSE");

  const color = isTrue
    ? "text-verdict-true"
    : isFalse
    ? "text-verdict-false"
    : "text-verdict-unverifiable";

  const bgColor = isTrue
    ? "bg-verdict-true/10 border-verdict-true/30"
    : isFalse
    ? "bg-verdict-false/10 border-verdict-false/30"
    : "bg-verdict-unverifiable/10 border-verdict-unverifiable/30";

  const Icon = isTrue ? ShieldCheck : isFalse ? ShieldX : ShieldQuestion;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className={`rounded-2xl border p-6 md:p-8 ${bgColor}`}
    >
      <div className="flex flex-col items-center gap-4 md:flex-row md:gap-8">
        <div className="flex flex-col items-center gap-2">
          <Icon className={`h-16 w-16 ${color}`} />
          <span className={`text-2xl font-extrabold uppercase tracking-wide ${color}`}>
            {verdict}
          </span>
        </div>
        <div className="flex-1 w-full space-y-4">
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-muted-foreground">Credibility Score</span>
              <span className="font-semibold">{credibilityScore}/100</span>
            </div>
            <Progress value={credibilityScore} className="h-3 rounded-full" />
          </div>
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-muted-foreground">Confidence</span>
              <span className="font-semibold">{confidence}%</span>
            </div>
            <Progress value={confidence} className="h-3 rounded-full" />
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default VerdictCard;
