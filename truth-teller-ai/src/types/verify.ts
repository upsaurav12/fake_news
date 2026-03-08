export interface VerifyResponse {
  extracted: {
    main_claim: string;
    keywords: string[];
    entities: string[];
    claim_type: string;
    search_query: string;
    time_context: string | null;
  };
  articles: {
    title: string;
    source: string;
    description: string;
    url: string;
    published_at: string;
  }[];
  analysis: {
    verdict: string;
    credibility_score: number;
    confidence: number;
    reasoning: string;
    red_flags: string[];
    supporting_points: string[];
    source_quality: string;
    claim_type_analysis: string;
    recommendation: string;
  };
}
