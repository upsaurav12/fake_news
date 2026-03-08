import { useState, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import Header from "@/components/Header";
import HeroInput from "@/components/HeroInput";
import VerdictCard from "@/components/VerdictCard";
import ClaimBreakdown from "@/components/ClaimBreakdown";
import ArticlesList from "@/components/ArticlesList";
import AnalysisInsights from "@/components/AnalysisInsights";
import ResultsSkeleton from "@/components/ResultsSkeleton";
import { useToast } from "@/hooks/use-toast";
import type { VerifyResponse } from "@/types/verify";

const Index = () => {
  const [isDark, setIsDark] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<VerifyResponse | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDark);
  }, [isDark]);

  // Set dark mode on mount
  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  const handleVerify = async (text: string) => {
    setIsLoading(true);
    setResult(null);
    try {
      const res = await fetch("http://localhost:8000/api/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data: VerifyResponse = await res.json();
      setResult(data);
    } catch (err: unknown) {
      toast({
        title: "Verification Failed",
        description: err instanceof Error ? err.message : "Could not reach the verification server.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header isDark={isDark} onToggleTheme={() => setIsDark(!isDark)} />
      <HeroInput onSubmit={handleVerify} isLoading={isLoading} />

      <AnimatePresence>
        {isLoading && (
          <motion.div key="skeleton" exit={{ opacity: 0 }}>
            <ResultsSkeleton />
          </motion.div>
        )}

        {result && !isLoading && (
          <motion.div
            key="results"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="container max-w-4xl space-y-8 pb-20"
          >
            <VerdictCard
              verdict={result.analysis.verdict}
              credibilityScore={result.analysis.credibility_score}
              confidence={result.analysis.confidence}
            />
            <ClaimBreakdown
              mainClaim={result.extracted.main_claim}
              keywords={result.extracted.keywords}
              entities={result.extracted.entities}
              claimType={result.extracted.claim_type}
              searchQuery={result.extracted.search_query}
              timeContext={result.extracted.time_context}
            />
            <ArticlesList articles={result.articles} />
            <AnalysisInsights
              reasoning={result.analysis.reasoning}
              redFlags={result.analysis.red_flags}
              supportingPoints={result.analysis.supporting_points}
              sourceQuality={result.analysis.source_quality}
              claimTypeAnalysis={result.analysis.claim_type_analysis}
              recommendation={result.analysis.recommendation}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Index;
