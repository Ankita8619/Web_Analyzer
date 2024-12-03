import puppeteer from "puppeteer";
import lighthouse from "lighthouse";
import { URL } from "url";

export async function runLighthouse(url) {
    try {
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        await page.goto(url);

        const { lhr } = await lighthouse(url, {
            port: new URL(browser.wsEndpoint()).port,
            output: "json",
            onlyCategories: ["performance", "accessibility"],
        });

        await browser.close();

        // Extract desired metrics
        const performance = Math.round(lhr.categories.performance.score * 100);
        const accessibility = Math.round(lhr.categories.accessibility.score * 100);
        const audits = lhr.audits;

        // Example: Get CSS/JS sizes
        const cssSize = audits["total-byte-weight"].details.items.find(item =>
            item.url.endsWith(".css")
        )?.totalBytes ?? 0;

        const jsSize = audits["total-byte-weight"].details.items.find(item =>
            item.url.endsWith(".js")
        )?.totalBytes ?? 0;

        return {
            numericalData: {
                performance,
                accessibility,
                cssSize: Math.round(cssSize / 1024), // Convert to KB
                jsSize: Math.round(jsSize / 1024), // Convert to KB
            },
            oneLiner: {
                performance: performance > 80 ? "Excellent performance" : "Needs improvement",
                accessibility:
                    accessibility > 80 ? "Great accessibility" : "Accessibility needs improvement",
                cssSize: cssSize < 500 * 1024 ? "Optimized CSS size" : "CSS size is too large",
                jsSize: jsSize < 1000 * 1024 ? "Optimized JS size" : "JS size is too large",
            },
            totalScore: performance * 0.5 + accessibility * 0.3 + (500 - cssSize / 1024) * 0.1,
        };
    } catch (error) {
        console.error("Error running Lighthouse:", error);
        return null;
    }
}
