import { useState } from "react";
import { motion } from "framer-motion";
import { Search, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface HeroInputProps {
  onSubmit: (text: string) => void;
  isLoading: boolean;
}

const HeroInput = ({ onSubmit, isLoading }: HeroInputProps) => {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    if (text.trim()) onSubmit(text.trim());
  };

  return (
    <section className="py-16 md:py-24">
      <div className="container max-w-3xl text-center">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-extrabold tracking-tight md:text-5xl lg:text-6xl"
        >
          Verify Any Claim with{" "}
          <span className="text-gradient">AI Precision</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mt-4 text-lg text-muted-foreground"
        >
          Paste a news headline, social media post, or any claim — get instant AI-powered fact-checking.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-8 space-y-4"
        >
          <Textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste news or claim to verify..."
            className="min-h-[140px] resize-none rounded-2xl border-border bg-card text-base shadow-lg focus-visible:ring-primary"
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) handleSubmit();
            }}
          />
          <Button
            onClick={handleSubmit}
            disabled={isLoading || !text.trim()}
            size="lg"
            className="rounded-full px-8 text-base font-semibold glow-primary"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Search className="mr-2 h-5 w-5" />
                Verify Claim
              </>
            )}
          </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroInput;
