import { Moon, Sun, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  isDark: boolean;
  onToggleTheme: () => void;
}

const Header = ({ isDark, onToggleTheme }: HeaderProps) => {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-xl">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold tracking-tight">
            Truth<span className="text-gradient">Check</span>
          </span>
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleTheme}
          className="rounded-full"
        >
          {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </Button>
      </div>
    </header>
  );
};

export default Header;
