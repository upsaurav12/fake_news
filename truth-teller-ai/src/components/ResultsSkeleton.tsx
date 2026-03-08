import { Skeleton } from "@/components/ui/skeleton";

const ResultsSkeleton = () => (
  <div className="container max-w-4xl space-y-6 py-8">
    <Skeleton className="h-40 w-full rounded-2xl" />
    <Skeleton className="h-56 w-full rounded-2xl" />
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {[1, 2, 3].map((i) => (
        <Skeleton key={i} className="h-40 rounded-2xl" />
      ))}
    </div>
    <Skeleton className="h-32 w-full rounded-2xl" />
  </div>
);

export default ResultsSkeleton;
