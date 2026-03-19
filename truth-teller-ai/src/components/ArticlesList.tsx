import { motion } from "framer-motion";
import { ExternalLink } from "lucide-react";
import { useState } from "react";

interface Article {
  title: string;
  source: string;
  description: string;
  url: string;
  published_at: string;
}

const ArticleCard = ({ article, index }: { article: Article; index: number }) => {
  const [expanded, setExpanded] = useState(false);
  const isLong = article.description.length > 120;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.05 * index }}
      className="rounded-2xl border border-border bg-card p-5 flex flex-col justify-between hover:border-primary/30 transition-colors"
    >
      <div>
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="font-semibold text-foreground hover:text-primary transition-colors inline-flex items-start gap-1"
        >
          {article.title}
          <ExternalLink className="h-3.5 w-3.5 mt-1 shrink-0" />
        </a>
        <p className="text-sm text-muted-foreground mt-2">
          {isLong && !expanded ? article.description.slice(0, 120) + "..." : article.description}
          {isLong && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="ml-1 text-primary text-xs font-medium hover:underline"
            >
              {expanded ? "show less" : "read more"}
            </button>
          )}
        </p>
      </div>
      <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
        <span className="font-medium">{article.source}</span>
        <span>{new Date(article.published_at).toLocaleDateString()}</span>
      </div>
    </motion.div>
  );
};

const ArticlesList = ({ articles }: { articles: Article[] }) => {
  if (!articles.length) return null;
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <h3 className="text-lg font-bold mb-4">Related Articles</h3>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {articles.map((a, i) => (
          <ArticleCard key={i} article={a} index={i} />
        ))}
      </div>
    </motion.div>
  );
};

export default ArticlesList;
