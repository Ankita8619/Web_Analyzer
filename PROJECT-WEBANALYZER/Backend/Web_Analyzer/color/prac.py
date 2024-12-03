import asyncio
from playwright.async_api import async_playwright

# JavaScript code to count text alignments
js_code = """
let alignmentCounts = { left: 0, center: 0, right: 0 };
document.querySelectorAll('*').forEach(element => {
    const styles = window.getComputedStyle(element);
    const textAlign = styles.textAlign;
    if (textAlign === 'left' || textAlign === 'start') alignmentCounts.left += 1;
    else if (textAlign === 'center') alignmentCounts.center += 1;
    else if (textAlign === 'right' || textAlign === 'end') alignmentCounts.right += 1;
});
alignmentCounts;  // Return the result directly here
"""

async def run_js_consistency_checks(html_content):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html_content)
        # Evaluate the JS code and capture the result
        consistency_report = await page.evaluate(js_code)
        await browser.close()
        return consistency_report

# Example HTML content
html_content = "<html><body><div style='text-align:left'>Left</div><div style='text-align:center'>Center</div><div style='text-align:right'>Right</div></body></html>"

# Running the checks
result = asyncio.run(run_js_consistency_checks(html_content))
print(result)
