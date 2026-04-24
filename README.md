# UK Electricity Index NationBuilder package

This zip includes both the self-contained NationBuilder embed files and a `full-source/` folder with the raw data, reference PNGs, source scripts, and supporting assets used to rebuild the chart.

How the iframe embed works:
- `chart-page-template.html` is pasted into one dedicated NationBuilder chart page.
- `embed-iframe-snippet.html` is pasted into the page or document template where the chart should appear.
- The iframe loads that dedicated chart page inside the destination page, which keeps the chart isolated from NationBuilder theme CSS and means you only need to update one chart page if the chart changes later.

Files in this package:
- `chart-page-template.html`: paste this into the dedicated chart page `Template` tab.
- `embed-iframe-snippet.html`: paste this into the destination page `Template` tab after replacing `CHART_PAGE_URL`.
- `standalone-preview.html`: local preview copy of the chart page.
- `full-source/`: raw data, reference PNGs, source scripts, and supporting assets for rebuilding the chart outside NationBuilder.

Admin steps:
1. Create a new `Basic` page for the chart only. Suggested slug: `uk-electricity-index-chart`.
2. Open that page's `Template` tab. If NationBuilder asks, create a custom template first.
3. Turn on `Ignore layout template` so the chart page renders without the normal site header/footer.
4. Replace the template contents with `chart-page-template.html`, then save and publish.
5. Open the live chart page and copy its full URL.
6. Open the page or document template where the chart should appear and paste `embed-iframe-snippet.html`.
7. Replace `CHART_PAGE_URL` with the live chart page URL and save.
8. Preview the page and adjust the iframe height if you want it taller or shorter.

Uploads required:
- None for the recommended NationBuilder route.
- The `full-source/` folder is only needed if someone wants to edit or regenerate the chart outside NationBuilder.

Notes:
- Keep the dedicated chart page out of navigation if it only exists to be embedded.
- If you duplicate the chart page, keep a fresh iframe snippet for each live URL.
- Some PNG generator scripts expect the BRM font files locally. The interactive HTML files in this package do not depend on those fonts being installed.
