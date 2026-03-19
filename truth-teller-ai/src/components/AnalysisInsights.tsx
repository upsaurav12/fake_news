import { motion } from "framer-motion";
import { AlertTriangle, CheckCircle2, Info, ChevronDown, ChevronUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";

interface AnalysisInsightsProps {
  reasoning: string;
  redFlags: string[];
  supportingPoints: string[];
  sourceQuality: string;
  claimTypeAnalysis: string;
  recommendation: string;
}

const AnalysisInsights = ({
  reasoning,
  redFlags,
  supportingPoints,
  sourceQuality,
  claimTypeAnalysis,
  recommendation,
}: AnalysisInsightsProps) => {
  const [reasoningExpanded, setReasoningExpanded] = useState(false);
  const isLongReasoning = reasoning.length > 300;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="space-y-6"
    >
      <h3 className="text-lg font-bold">Analysis Insights</h3>

      {/* Reasoning */}
      <div className="rounded-2xl border border-border bg-card p-5 space-y-2">
        <div className="flex items-center gap-2 text-sm font-semibold text-muted-foreground">
          <Info className="h-4 w-4" />
          Reasoning
        </div>
        <p className="text-sm leading-relaxed">
          {isLongReasoning && !reasoningExpanded ? reasoning.slice(0, 300) + "..." : reasoning}
        </p>
        {isLongReasoning && (
          <button
            onClick={() => setReasoningExpanded(!reasoningExpanded)}
            className="text-primary text-xs font-medium flex items-center gap-1 hover:underline"
          >
            {reasoningExpanded ? (
              <>Show less <ChevronUp className="h-3 w-3" /></>
            ) : (
              <>Read more <ChevronDown className="h-3 w-3" /></>
            )}
          </button>
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {/* Supporting Points */}
        {supportingPoints.length > 0 && (
          <div className="rounded-2xl border border-border bg-card p-5 space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-verdict-true">
              <CheckCircle2 className="h-4 w-4" />
              Supporting Points
            </div>
            <ul className="space-y-1.5">
              {supportingPoints.map((p, i) => (
                <li key={i} className="text-sm text-muted-foreground flex gap-2">
                  <span className="text-verdict-true mt-0.5">•</span>
                  {p}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Red Flags */}
        {redFlags.length > 0 && (
          <div className="rounded-2xl border border-border bg-card p-5 space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-verdict-false">
              <AlertTriangle className="h-4 w-4" />
              Red Flags
            </div>
            <div className="flex flex-wrap gap-1.5">
              {redFlags.map((f, i) => (
                <Badge key={i} variant="destructive" className="rounded-full text-xs">
                  {f}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Source Quality & Claim Type */}
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl border border-border bg-card p-5">
          <p className="text-sm text-muted-foreground mb-1">Source Quality</p>
          <p className="text-sm font-medium">{sourceQuality}</p>
        </div>
        <div className="rounded-2xl border border-border bg-card p-5">
          <p className="text-sm text-muted-foreground mb-1">Claim Type Analysis</p>
          <p className="text-sm font-medium">{claimTypeAnalysis}</p>
        </div>
      </div>

      {/* Recommendation */}
      <div className="rounded-2xl border-2 border-primary/30 bg-accent p-5">
        <p className="text-sm font-semibold text-accent-foreground mb-1">💡 Recommendation</p>
        <p className="text-sm text-accent-foreground/80">{recommendation}</p>
      </div>
    </motion.div>
  );
};

export default AnalysisInsights;
