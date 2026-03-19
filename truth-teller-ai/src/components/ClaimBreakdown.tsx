import { motion } from "framer-motion";
import { Copy, Check } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";

interface ClaimBreakdownProps {
  mainClaim: string;
  keywords: string[];
  entities: string[];
  claimType: string;
  searchQuery: string;
  timeContext: string | null;
}

const ClaimBreakdown = ({ mainClaim, keywords, entities, claimType, searchQuery, timeContext }: ClaimBreakdownProps) => {
  const [copied, setCopied] = useState(false);

  const copyQuery = () => {
    navigator.clipboard.writeText(searchQuery);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="rounded-2xl border border-border bg-card p-6 space-y-4"
    >
      <h3 className="text-lg font-bold">Claim Breakdown</h3>
      <div>
        <p className="text-sm text-muted-foreground mb-1">Main Claim</p>
        <p className="font-medium">{mainClaim}</p>
      </div>
      <div className="flex flex-wrap gap-4">
        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">Keywords</p>
          <div className="flex flex-wrap gap-1.5">
            {keywords.map((k) => (
              <Badge key={k} variant="secondary" className="rounded-full">{k}</Badge>
            ))}
          </div>
        </div>
        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">Entities</p>
          <div className="flex flex-wrap gap-1.5">
            {entities.map((e) => (
              <Badge key={e} variant="outline" className="rounded-full">{e}</Badge>
            ))}
          </div>
        </div>
      </div>
      <div className="flex flex-wrap gap-6 text-sm">
        <div>
          <span className="text-muted-foreground">Claim Type: </span>
          <span className="font-medium">{claimType}</span>
        </div>
        {timeContext && (
          <div>
            <span className="text-muted-foreground">Time Context: </span>
            <span className="font-medium">{timeContext}</span>
          </div>
        )}
      </div>
      <div>
        <p className="text-sm text-muted-foreground mb-1">Search Query</p>
        <div className="flex items-center gap-2 rounded-lg bg-muted p-3">
          <code className="flex-1 text-sm font-mono text-accent-foreground">{searchQuery}</code>
          <button onClick={copyQuery} className="text-muted-foreground hover:text-foreground transition-colors">
            {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default ClaimBreakdown;
