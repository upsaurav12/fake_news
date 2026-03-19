import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"\n✓ TruthCheck Python backend starting on http://localhost:{port}")
    print(f"  ANTHROPIC_API_KEY : {'✓ set' if os.getenv('ANTHROPIC_API_KEY') else '✗ missing'}")
    print(f"  NEWS_API_KEY      : {'✓ set' if os.getenv('NEWS_API_KEY') else '✗ missing'}")
    print(f"\n  API docs          : http://localhost:{port}/docs\n")

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
