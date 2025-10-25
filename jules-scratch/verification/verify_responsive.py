import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get the absolute path to the index.html file
        html_file_path = os.path.abspath('index.html')

        await page.goto(f'file://{html_file_path}')

        screenshots = []

        # Mobile
        await page.set_viewport_size({"width": 375, "height": 667})
        mobile_screenshot_path = "jules-scratch/verification/mobile.png"
        await page.screenshot(path=mobile_screenshot_path)
        screenshots.append(mobile_screenshot_path)

        # Tablet
        await page.set_viewport_size({"width": 768, "height": 1024})
        tablet_screenshot_path = "jules-scratch/verification/tablet.png"
        await page.screenshot(path=tablet_screenshot_path)
        screenshots.append(tablet_screenshot_path)

        # Desktop
        await page.set_viewport_size({"width": 1280, "height": 800})
        desktop_screenshot_path = "jules-scratch/verification/desktop.png"
        await page.screenshot(path=desktop_screenshot_path)
        screenshots.append(desktop_screenshot_path)

        await browser.close()

        # Combine screenshots into one image for easier viewing
        from PIL import Image
        images = [Image.open(x) for x in screenshots]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]

        combined_screenshot_path = "jules-scratch/verification/responsive_screenshots.png"
        new_im.save(combined_screenshot_path)
        print(f"Screenshots saved and combined into {combined_screenshot_path}")

if __name__ == "__main__":
    asyncio.run(main())
