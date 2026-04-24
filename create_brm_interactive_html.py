import base64
import json
from pathlib import Path

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

DATA_CSV_PATH = ROOT_DIR / "raw-data" / "uk-electricity-index" / "datawrapper_brm_electricity_index_2000_2019.csv"
LOGO_PATH = ROOT_DIR / "brand-assets" / "logos" / "BRM-Logo-Colour@2x.png"
OUTPUT_HTML_PATH = ROOT_DIR / "interactive-charts" / "uk-electricity-index" / "preview" / "brm_uk_electricity_index_chart_interactive.html"

BR_RED = "#E8000D"
BR_BLUE = "#2161FF"
BR_NAVY = "#000032"
BR_BLACK = "#000000"
BR_GREY = "#F2F2F2"
GRID_GREY = "#D9DDE6"
SECONDARY_LINE = "#AEB8CC"


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Britain Remade Interactive Electricity Demand Chart</title>
  <style>
    @font-face {{
      font-family: "FS Elliot";
      src: local("FS Elliot"), local("FSElliot");
      font-weight: 400;
    }}
    @font-face {{
      font-family: "FS Elliot";
      src: local("FS Elliot Bold"), local("FSElliot-Bold"), local("FS Elliot");
      font-weight: 700;
    }}
    :root {{
      --br-red: __BR_RED__;
      --br-blue: __BR_BLUE__;
      --br-navy: __BR_NAVY__;
      --br-black: __BR_BLACK__;
      --br-grey: __BR_GREY__;
      --grid-grey: __GRID_GREY__;
      --secondary-line: __SECONDARY_LINE__;
      --paper: #ffffff;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--br-black);
      font-family: "FS Elliot", "Helvetica Neue", Arial, sans-serif;
    }}
    .page {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 16px 18px 24px;
    }}
    .top-rule {{
      height: 2px;
      width: 100%;
      background: var(--br-navy);
      margin-bottom: 18px;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 24px;
      margin-bottom: 14px;
    }}
    .headline-block {{
      flex: 1 1 920px;
      min-width: 0;
      max-width: 980px;
    }}
    .headline {{
      margin: 0;
      font-size: clamp(22px, 2.4vw, 34px);
      line-height: 1.04;
      font-weight: 700;
      letter-spacing: -0.03em;
      max-width: none;
    }}
    .subhead {{
      margin: 12px 0 0;
      font-size: clamp(16px, 1.7vw, 20px);
      line-height: 1.1;
      font-weight: 400;
      letter-spacing: -0.02em;
      max-width: 900px;
    }}
    .header-side {{
      width: min(260px, 21vw);
      min-width: 180px;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 10px;
    }}
    .controls {{
      width: 100%;
      display: flex;
      gap: 8px;
      align-items: stretch;
      justify-content: flex-end;
    }}
    .search {{
      flex: 1 1 auto;
      min-width: 0;
      border: 1px solid #cfd5e0;
      border-radius: 0;
      padding: 10px 12px;
      font: inherit;
      font-size: 15px;
      color: var(--br-black);
      background: #fff;
    }}
    .search:focus {{
      outline: 2px solid rgba(33, 97, 255, 0.18);
      border-color: var(--br-blue);
    }}
    .clear-btn {{
      border: 0;
      border-radius: 0;
      background: var(--br-blue);
      color: #fff;
      font: inherit;
      font-weight: 700;
      padding: 0 14px;
      cursor: pointer;
    }}
    .hint {{
      width: 100%;
      text-align: right;
      font-size: 13px;
      color: rgba(0, 0, 50, 0.68);
    }}
    .chart-wrap {{
      position: relative;
      margin-top: 10px;
    }}
    #chart {{
      width: 100%;
      height: auto;
      display: block;
      overflow: visible;
    }}
    .tooltip {{
      position: absolute;
      display: none;
      min-width: 190px;
      max-width: 260px;
      pointer-events: none;
      z-index: 20;
      background: rgba(255, 255, 255, 0.98);
      border: 1px solid rgba(0, 0, 50, 0.12);
      box-shadow: 0 10px 24px rgba(0, 0, 50, 0.12);
      padding: 10px 12px;
      font-size: 14px;
      line-height: 1.25;
      color: var(--br-navy);
    }}
    .tooltip-title {{
      font-weight: 700;
      color: var(--br-black);
      margin-bottom: 4px;
    }}
    .footer {{
      margin-top: 14px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 18px;
      font-size: 12px;
      color: rgba(0, 0, 50, 0.62);
    }}
    .footer em {{
      font-style: italic;
    }}
    .footer-text {{
      flex: 1 1 auto;
      min-width: 0;
    }}
    .footer-logo {{
      width: min(160px, 16vw);
      min-width: 110px;
      height: auto;
      display: block;
      flex: 0 0 auto;
    }}
    @media (max-width: 1100px) {{
      .page {{
        padding: 14px 16px 22px;
      }}
      .header {{
        gap: 18px;
      }}
    }}
    @media (max-width: 900px) {{
      .header {{
        flex-direction: column;
      }}
      .header-side {{
        width: 100%;
        min-width: 0;
        align-items: flex-start;
      }}
      .controls {{
        max-width: 420px;
      }}
      .hint {{
        text-align: left;
      }}
      .headline {{
        max-width: none;
      }}
      .subhead {{
        max-width: none;
      }}
      .footer {{
        flex-direction: column;
        align-items: flex-start;
      }}
      .footer-logo {{
        align-self: flex-end;
      }}
    }}
    @media (max-width: 700px) {{
      .page {{
        padding: 12px 12px 18px;
      }}
      .top-rule {{
        margin-bottom: 14px;
      }}
      .header {{
        gap: 12px;
        margin-bottom: 10px;
      }}
      .controls {{
        gap: 6px;
      }}
      .search {{
        padding: 9px 10px;
        font-size: 14px;
      }}
      .clear-btn {{
        padding: 0 12px;
      }}
      .hint {{
        font-size: 12px;
      }}
      .footer {{
        font-size: 11px;
        gap: 10px;
      }}
      .footer-logo {{
        width: min(128px, 34vw);
        min-width: 92px;
      }}
    }}
    @media (max-width: 480px) {{
      .headline {{
        font-size: clamp(18px, 6.4vw, 26px);
        line-height: 1.05;
      }}
      .subhead {{
        margin-top: 8px;
        font-size: clamp(13px, 4.2vw, 16px);
        line-height: 1.15;
      }}
      .chart-wrap {{
        margin-top: 6px;
      }}
    }}
    @media (max-height: 500px) and (orientation: landscape) {{
      .page {{
        padding: 10px 10px 14px;
      }}
      .top-rule {{
        margin-bottom: 10px;
      }}
      .header {{
        flex-direction: row;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 8px;
      }}
      .headline-block {{
        flex: 1 1 auto;
        max-width: none;
      }}
      .headline {{
        font-size: clamp(18px, 3.1vw, 24px);
        line-height: 1.03;
      }}
      .subhead {{
        margin-top: 6px;
        font-size: clamp(12px, 1.9vw, 14px);
        line-height: 1.12;
      }}
      .header-side {{
        width: min(220px, 32vw);
        min-width: 170px;
        gap: 6px;
      }}
      .controls {{
        max-width: none;
        gap: 4px;
      }}
      .search {{
        padding: 8px 9px;
        font-size: 13px;
      }}
      .clear-btn {{
        padding: 0 10px;
        font-size: 13px;
      }}
      .hint {{
        font-size: 11px;
      }}
      .chart-wrap {{
        margin-top: 4px;
      }}
      .footer {{
        margin-top: 8px;
        font-size: 10px;
        gap: 8px;
      }}
      .footer-logo {{
        width: min(104px, 18vw);
        min-width: 72px;
      }}
    }}
    @media (orientation: portrait) and (max-width: 980px) {{
      .page {{
        padding-top: 18px;
        padding-bottom: 16px;
      }}
      .top-rule {{
        margin-bottom: 10px;
      }}
      .header {{
        display: block;
        margin-bottom: 8px;
      }}
      .headline {{
        font-size: clamp(18px, 5.6vw, 30px);
      }}
      .subhead {{
        margin-top: 8px;
        font-size: clamp(13px, 3.8vw, 17px);
      }}
      .header-side {{
        display: none;
      }}
      .chart-wrap {{
        margin-top: 0;
      }}
      .footer {{
        margin-top: 8px;
        gap: 8px;
      }}
      .footer-logo {{
        width: min(102px, 28vw);
        min-width: 68px;
        margin-left: auto;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="top-rule"></div>
    <div class="header">
      <div class="headline-block">
        <h1 class="headline">The UK has seen the largest fall in electricity demand per capita since 2000 of any OECD country</h1>
        <p class="subhead">Only Yemen, Zimbabwe, Jamaica, Tajikistan and Syria saw electricity demand drop by more</p>
      </div>
      <div class="header-side">
        <div class="controls">
          <input id="series-search" class="search" list="series-list" type="search" placeholder="Find a country">
          <button id="clear-search" class="clear-btn" type="button">Clear</button>
        </div>
        <div class="hint" id="interaction-hint">Tap or hover lines to inspect values, or search to highlight a country.</div>
      </div>
    </div>

    <div class="chart-wrap" id="chart-wrap">
      <svg id="chart" viewBox="0 0 1400 640" preserveAspectRatio="xMidYMid meet" aria-label="Interactive line chart of indexed per-capita electricity demand"></svg>
      <div class="tooltip" id="tooltip"></div>
    </div>

    <div class="footer">
      <div class="footer-text">Source: Our World in Data, <em>Electricity Demand Per Capita</em> (2000-2019), 2000 = 100</div>
      <img class="footer-logo" alt="Britain Remade" src="data:image/png;base64,__LOGO_DATA__">
    </div>
    <datalist id="series-list"></datalist>
  </div>

  <script>
    const payload = __DATA_PAYLOAD__;

    const BR_RED = "__BR_RED__";
    const BR_BLUE = "__BR_BLUE__";
    const BR_NAVY = "__BR_NAVY__";
    const BR_BLACK = "__BR_BLACK__";
    const GRID_GREY = "__GRID_GREY__";
    const SECONDARY_LINE = "__SECONDARY_LINE__";

    const svg = document.getElementById("chart");
    const tooltip = document.getElementById("tooltip");
    const chartWrap = document.getElementById("chart-wrap");
    const searchInput = document.getElementById("series-search");
    const clearButton = document.getElementById("clear-search");
    const datalist = document.getElementById("series-list");
    const hint = document.getElementById("interaction-hint");

    const yTicks = [50, 100, 200, 500, 1000, 2000];
    const years = payload.years;
    const xMin = years[0];
    const xMax = years[years.length - 1];
    const logMin = Math.log(40);
    const logMax = Math.log(2200);
    const seriesByName = new Map(payload.series.map((s) => [s.name, s]));
    const seriesNodes = new Map();

    let selectedName = null;
    let hoverName = null;
    let currentLayout = null;
    let updateState = () => {};
    let renderFrame = null;

    function getLayout() {
      const containerWidth = Math.max(chartWrap.clientWidth || window.innerWidth || 320, 320);
      const viewportWidth = Math.max(window.innerWidth || containerWidth, containerWidth);
      const viewportHeight = Math.max(window.innerHeight || 0, 240);
      const isPortrait = viewportHeight >= viewportWidth;
      const isShortLandscape = viewportWidth > viewportHeight && viewportHeight <= 500 && viewportWidth <= 950;
      let layout;

      if (isShortLandscape) {
        layout = {
          mode: "phone-landscape",
          width: 980,
          height: 340,
          margin: { top: 14, right: 132, bottom: 42, left: 44 },
          xTicks: [2000, 2005, 2010, 2015, 2019],
          axisFontSize: 10,
          labelFontSize: 9.5,
          labelPaddingX: 6,
          labelPaddingY: 3,
          labelGap: 20,
          labelMode: "inside",
          labelOffsetX: 10,
          focusLabelOffsetY: -12,
          endpointRadius: 3.4,
          otherLineWidth: 0.95,
          otherOpacity: 0.28,
          otherHitWidth: 14,
          specialHitWidth: 18
        };
      } else if (containerWidth <= 640 && isPortrait) {
        layout = {
          mode: "phone-portrait",
          width: 780,
          height: 1040,
          margin: { top: 14, right: 16, bottom: 54, left: 44 },
          xTicks: [2000, 2010, 2019],
          axisFontSize: 10.5,
          labelFontSize: 10,
          labelPaddingX: 7,
          labelPaddingY: 4,
          labelGap: 22,
          labelMode: "inside",
          labelOffsetX: 10,
          focusLabelOffsetY: -12,
          endpointRadius: 3.8,
          otherLineWidth: 1.05,
          otherOpacity: 0.28,
          otherHitWidth: 16,
          specialHitWidth: 22
        };
      } else if (containerWidth <= 640) {
        layout = {
          mode: "phone",
          width: 780,
          height: 620,
          margin: { top: 16, right: 18, bottom: 56, left: 46 },
          xTicks: [2000, 2010, 2019],
          axisFontSize: 11,
          labelFontSize: 10,
          labelPaddingX: 7,
          labelPaddingY: 4,
          labelGap: 22,
          labelMode: "inside",
          labelOffsetX: 10,
          focusLabelOffsetY: -12,
          endpointRadius: 3.8,
          otherLineWidth: 1.1,
          otherOpacity: 0.29,
          otherHitWidth: 16,
          specialHitWidth: 22
        };
      } else if (containerWidth <= 980 && isPortrait) {
        layout = {
          mode: "tablet-portrait",
          width: 1100,
          height: 1100,
          margin: { top: 18, right: 138, bottom: 54, left: 58 },
          xTicks: [2000, 2005, 2010, 2015, 2019],
          axisFontSize: 11,
          labelFontSize: 10.5,
          labelPaddingX: 7,
          labelPaddingY: 4,
          labelGap: 24,
          labelMode: "outside",
          labelOffsetX: 16,
          focusLabelOffsetY: -15,
          endpointRadius: 4,
          otherLineWidth: 1,
          otherOpacity: 0.31,
          otherHitWidth: 13,
          specialHitWidth: 18
        };
      } else if (containerWidth <= 980) {
        layout = {
          mode: "tablet",
          width: 1100,
          height: 760,
          margin: { top: 20, right: 150, bottom: 56, left: 60 },
          xTicks: [2000, 2005, 2010, 2015, 2019],
          axisFontSize: 11,
          labelFontSize: 10.5,
          labelPaddingX: 7,
          labelPaddingY: 4,
          labelGap: 25,
          labelMode: "outside",
          labelOffsetX: 16,
          focusLabelOffsetY: -16,
          endpointRadius: 4,
          otherLineWidth: 1,
          otherOpacity: 0.33,
          otherHitWidth: 13,
          specialHitWidth: 18
        };
      } else {
        layout = {
          mode: "desktop",
          width: 1400,
          height: 640,
          margin: { top: 24, right: 185, bottom: 52, left: 72 },
          xTicks: [2000, 2005, 2010, 2015, 2019],
          axisFontSize: 12,
          labelFontSize: 11,
          labelPaddingX: 8,
          labelPaddingY: 4,
          labelGap: 26,
          labelMode: "outside",
          labelOffsetX: 18,
          focusLabelOffsetY: -18,
          endpointRadius: 4.2,
          otherLineWidth: 1,
          otherOpacity: 0.34,
          otherHitWidth: 12,
          specialHitWidth: 18
        };
      }

      layout.plotWidth = layout.width - layout.margin.left - layout.margin.right;
      layout.plotHeight = layout.height - layout.margin.top - layout.margin.bottom;
      return layout;
    }

    function svgEl(tag, attrs = {}, parent = null) {
      const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
      Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
      if (parent) parent.appendChild(el);
      return el;
    }

    function xScale(year) {
      return currentLayout.margin.left + ((year - xMin) / (xMax - xMin)) * currentLayout.plotWidth;
    }

    function yScale(value) {
      const logged = Math.log(value);
      return currentLayout.margin.top + (1 - (logged - logMin) / (logMax - logMin)) * currentLayout.plotHeight;
    }

    function linePath(values) {
      let d = "";
      let drawing = false;
      values.forEach((value, index) => {
        if (value === null || Number.isNaN(value)) {
          drawing = false;
          return;
        }
        const x = xScale(years[index]).toFixed(2);
        const y = yScale(value).toFixed(2);
        d += drawing ? ` L ${x} ${y}` : `M ${x} ${y}`;
        drawing = true;
      });
      return d;
    }

    function lastPoint(series) {
      for (let i = series.values.length - 1; i >= 0; i -= 1) {
        const value = series.values[i];
        if (value !== null && !Number.isNaN(value)) {
          return { year: years[i], value };
        }
      }
      return null;
    }

    function formatValue(value) {
      return value.toFixed(1);
    }

    function formatChange(value) {
      const diff = value - 100;
      const sign = diff > 0 ? "+" : "";
      return `${sign}${diff.toFixed(1)}`;
    }

    function nearestDefinedPoint(series, svgX) {
      const ratio = Math.max(0, Math.min(1, (svgX - currentLayout.margin.left) / currentLayout.plotWidth));
      let index = Math.round(ratio * (years.length - 1));
      if (series.values[index] !== null && !Number.isNaN(series.values[index])) {
        return { year: years[index], value: series.values[index] };
      }

      for (let offset = 1; offset < years.length; offset += 1) {
        const left = index - offset;
        const right = index + offset;
        if (left >= 0 && series.values[left] !== null && !Number.isNaN(series.values[left])) {
          return { year: years[left], value: series.values[left] };
        }
        if (right < years.length && series.values[right] !== null && !Number.isNaN(series.values[right])) {
          return { year: years[right], value: series.values[right] };
        }
      }
      return null;
    }

    function activeSeries() {
      return hoverName ? seriesByName.get(hoverName) : selectedName ? seriesByName.get(selectedName) : null;
    }

    function specialStyle(kind) {
      if (kind === "uk") return { color: BR_RED, width: currentLayout.mode === "phone" ? 3.6 : 4 };
      if (kind === "oecd") return { color: BR_BLUE, width: currentLayout.mode === "phone" ? 3.1 : 3.4 };
      return { color: BR_NAVY, width: currentLayout.mode === "phone" ? 3.1 : 3.4 };
    }

    function drawAxes(root) {
      const { margin, width, height, xTicks, axisFontSize } = currentLayout;

      yTicks.forEach((tick) => {
        const y = yScale(tick);
        svgEl("line", {
          x1: margin.left,
          x2: width - margin.right,
          y1: y,
          y2: y,
          stroke: GRID_GREY,
          "stroke-width": 1
        }, root);

        const label = svgEl("text", {
          x: margin.left - 12,
          y: y + 5,
          "text-anchor": "end",
          fill: BR_NAVY,
          "font-size": axisFontSize,
          "font-weight": tick === 100 ? 700 : 400
        }, root);
        label.textContent = tick;
      });

      xTicks.forEach((tick) => {
        const x = xScale(tick);
        const label = svgEl("text", {
          x,
          y: height - margin.bottom + 22,
          "text-anchor": tick === xTicks[0] ? "start" : tick === xTicks[xTicks.length - 1] ? "end" : "middle",
          fill: BR_NAVY,
          "font-size": axisFontSize,
          "font-weight": 700
        }, root);
        label.textContent = tick;
      });
    }

    function drawEndLabel(layer, text, color, x, y, options = {}) {
      const {
        anchor = "start",
        fontSize = currentLayout.labelFontSize,
        paddingX = currentLayout.labelPaddingX,
        paddingY = currentLayout.labelPaddingY
      } = options;

      const group = svgEl("g", {}, layer);
      const labelText = svgEl("text", {
        x,
        y,
        fill: "#ffffff",
        "font-size": fontSize,
        "font-weight": 700,
        "text-anchor": anchor,
        "dominant-baseline": "middle"
      }, group);
      labelText.textContent = text.toUpperCase();

      const bbox = labelText.getBBox();
      const rect = svgEl("rect", {
        x: bbox.x - paddingX,
        y: bbox.y - paddingY,
        width: bbox.width + paddingX * 2,
        height: bbox.height + paddingY * 2,
        fill: color
      }, group);
      group.insertBefore(rect, labelText);
      return group;
    }

    function labelAnchor() {
      return currentLayout.labelMode === "inside" ? "end" : "start";
    }

    function labelX(point) {
      return currentLayout.labelMode === "inside"
        ? currentLayout.width - currentLayout.margin.right - 8
        : xScale(point.year) + currentLayout.labelOffsetX;
    }

    function computeLabelPositions(definitions) {
      const positioned = definitions
        .map((definition) => {
          const point = lastPoint(definition.series);
          if (!point) return null;
          return {
            ...definition,
            point,
            targetY: yScale(point.value) + (definition.offsetY || 0)
          };
        })
        .filter(Boolean)
        .sort((a, b) => a.targetY - b.targetY);

      if (!positioned.length) return [];

      const minY = currentLayout.margin.top + 12;
      const maxY = currentLayout.height - currentLayout.margin.bottom - 12;
      positioned[0].y = Math.max(positioned[0].targetY, minY);

      for (let index = 1; index < positioned.length; index += 1) {
        positioned[index].y = Math.max(positioned[index].targetY, positioned[index - 1].y + currentLayout.labelGap);
      }

      const overflow = positioned[positioned.length - 1].y - maxY;
      if (overflow > 0) {
        positioned[positioned.length - 1].y -= overflow;
        for (let index = positioned.length - 2; index >= 0; index -= 1) {
          positioned[index].y = Math.min(positioned[index].y, positioned[index + 1].y - currentLayout.labelGap);
        }
        if (positioned[0].y < minY) {
          const shift = minY - positioned[0].y;
          positioned.forEach((item) => {
            item.y += shift;
          });
        }
      }

      return positioned.map((item) => ({
        ...item,
        x: labelX(item.point),
        anchor: labelAnchor()
      }));
    }

    function showTooltip(event, series, svgX) {
      const point = nearestDefinedPoint(series, svgX) || lastPoint(series);
      if (!point) return;
      tooltip.innerHTML = `
          <div class="tooltip-title">${series.name}</div>
          <div>${point.year}: ${formatValue(point.value)} (2000 = 100)</div>
          <div>${formatChange(point.value)} since 2000</div>
        `;
      tooltip.style.display = "block";

      const wrapRect = chartWrap.getBoundingClientRect();
      let left = event.clientX - wrapRect.left + 16;
      let top = event.clientY - wrapRect.top + 16;
      requestAnimationFrame(() => {
        const tooltipRect = tooltip.getBoundingClientRect();
        if (left + tooltipRect.width > wrapRect.width - 12) {
          left = wrapRect.width - tooltipRect.width - 12;
        }
        if (top + tooltipRect.height > wrapRect.height - 12) {
          top = wrapRect.height - tooltipRect.height - 12;
        }
        tooltip.style.left = `${Math.max(12, left)}px`;
        tooltip.style.top = `${Math.max(12, top)}px`;
      });
    }

    function hideTooltip() {
      tooltip.style.display = "none";
    }

    function render() {
      currentLayout = getLayout();
      svg.setAttribute("viewBox", `0 0 ${currentLayout.width} ${currentLayout.height}`);
      hint.textContent = (currentLayout.mode === "phone" || currentLayout.mode === "phone-portrait" || currentLayout.mode === "phone-landscape")
        ? "Tap lines to inspect values, or search to highlight a country."
        : "Tap or hover lines to inspect values, or search to highlight a country.";

      svg.innerHTML = "";
      seriesNodes.clear();

      const axisLayer = svgEl("g", {}, svg);
      const otherLayer = svgEl("g", {}, svg);
      const specialLayer = svgEl("g", {}, svg);
      const focusLayer = svgEl("g", {}, svg);
      const interactionLayer = svgEl("g", {}, svg);
      const labelLayer = svgEl("g", {}, svg);

      drawAxes(axisLayer);

      payload.series.forEach((series) => {
        const d = linePath(series.values);
        if (!d) return;

        const layer = series.kind === "other" ? otherLayer : specialLayer;
        const style = series.kind === "other"
          ? { color: SECONDARY_LINE, width: currentLayout.otherLineWidth, opacity: currentLayout.otherOpacity }
          : { ...specialStyle(series.kind), opacity: 1 };

        const visible = svgEl("path", {
          d,
          fill: "none",
          stroke: style.color,
          "stroke-width": style.width,
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          opacity: style.opacity
        }, layer);

        const hit = svgEl("path", {
          d,
          fill: "none",
          stroke: "transparent",
          "stroke-width": series.kind === "other" ? currentLayout.otherHitWidth : currentLayout.specialHitWidth,
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          style: "pointer-events: stroke; cursor: pointer;"
        }, interactionLayer);

        hit.addEventListener("pointerenter", () => {
          hoverName = series.name;
          updateState();
        });

        hit.addEventListener("pointermove", (event) => {
          hoverName = series.name;
          const rect = svg.getBoundingClientRect();
          const svgX = ((event.clientX - rect.left) / rect.width) * currentLayout.width;
          showTooltip(event, series, svgX);
          updateState();
        });

        hit.addEventListener("pointerleave", () => {
          hoverName = null;
          hideTooltip();
          updateState();
        });

        hit.addEventListener("click", (event) => {
          selectedName = selectedName === series.name ? null : series.name;
          hoverName = selectedName ? series.name : null;
          if (selectedName) {
            const rect = svg.getBoundingClientRect();
            const svgX = ((event.clientX - rect.left) / rect.width) * currentLayout.width;
            showTooltip(event, series, svgX);
          } else {
            hideTooltip();
          }
          searchInput.value = selectedName || "";
          updateState();
        });

        seriesNodes.set(series.name, { series, visible });
      });

      ["Global average", "OECD average", "United Kingdom"]
        .map((name) => seriesByName.get(name))
        .filter(Boolean)
        .forEach((series) => {
          const point = lastPoint(series);
          if (!point) return;
          svgEl("circle", {
            cx: xScale(point.year),
            cy: yScale(point.value),
            r: currentLayout.endpointRadius,
            fill: specialStyle(series.kind).color
          }, labelLayer);
        });

      computeLabelPositions([
        { text: "GLOBAL AVERAGE", series: seriesByName.get("Global average"), color: BR_NAVY },
        { text: "OECD AVERAGE", series: seriesByName.get("OECD average"), color: BR_BLUE },
        { text: "UNITED KINGDOM", series: seriesByName.get("United Kingdom"), color: BR_RED }
      ]).forEach((item) => {
        drawEndLabel(labelLayer, item.text, item.color, item.x, item.y, { anchor: item.anchor });
      });

      const focusPath = svgEl("path", {
        fill: "none",
        stroke: BR_BLACK,
        "stroke-width": 2.8,
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        opacity: 0
      }, focusLayer);

      const focusDot = svgEl("circle", {
        r: currentLayout.endpointRadius,
        fill: BR_BLACK,
        opacity: 0
      }, focusLayer);

      let focusLabel = null;

      updateState = function() {
        const current = activeSeries();
        const dimOthers = current && current.kind === "other";

        payload.series.forEach((series) => {
          const node = seriesNodes.get(series.name);
          if (!node) return;
          const path = node.visible;
          if (series.kind === "other") {
            path.setAttribute("opacity", dimOthers ? (series.name === current.name ? 0.05 : 0.14) : currentLayout.otherOpacity);
          } else {
            const style = specialStyle(series.kind);
            const isActive = current && current.name === series.name;
            path.setAttribute("stroke-width", isActive ? style.width + 0.8 : style.width);
            path.setAttribute("opacity", isActive ? 1 : 0.98);
          }
        });

        if (focusLabel) {
          focusLabel.remove();
          focusLabel = null;
        }

        if (current && current.kind === "other") {
          focusPath.setAttribute("d", linePath(current.values));
          focusPath.setAttribute("opacity", 1);
          const point = lastPoint(current);
          focusDot.setAttribute("cx", xScale(point.year));
          focusDot.setAttribute("cy", yScale(point.value));
          focusDot.setAttribute("opacity", 1);

          if (selectedName === current.name && !hoverName) {
            focusLabel = drawEndLabel(
              focusLayer,
              current.name,
              BR_BLACK,
              labelX(point),
              yScale(point.value) + currentLayout.focusLabelOffsetY,
              { anchor: labelAnchor() }
            );
          }
        } else {
          focusPath.setAttribute("opacity", 0);
          focusDot.setAttribute("opacity", 0);
        }
      };

      updateState();
    }

    function scheduleRender() {
      if (renderFrame !== null) cancelAnimationFrame(renderFrame);
      renderFrame = requestAnimationFrame(() => {
        renderFrame = null;
        render();
      });
    }

    datalist.innerHTML = "";
    payload.series.forEach((series) => {
      const option = document.createElement("option");
      option.value = series.name;
      datalist.appendChild(option);
    });

    searchInput.addEventListener("input", () => {
      const raw = searchInput.value.trim().toLowerCase();
      if (!raw) {
        selectedName = null;
        hoverName = null;
        hideTooltip();
        updateState();
        return;
      }

      const exact = payload.series.find((series) => series.name.toLowerCase() === raw);
      if (exact) {
        selectedName = exact.name;
        hoverName = null;
        updateState();
        return;
      }

      const matches = payload.series.filter((series) => series.name.toLowerCase().startsWith(raw));
      selectedName = matches.length === 1 ? matches[0].name : null;
      hoverName = null;
      updateState();
    });

    clearButton.addEventListener("click", () => {
      searchInput.value = "";
      selectedName = null;
      hoverName = null;
      hideTooltip();
      updateState();
    });

    if (window.ResizeObserver) {
      const resizeObserver = new ResizeObserver(() => scheduleRender());
      resizeObserver.observe(chartWrap);
    }
    window.addEventListener("resize", scheduleRender);
    window.addEventListener("orientationchange", scheduleRender);

    render();
  </script>
</body>
</html>
"""


def build_payload():
    df = pd.read_csv(DATA_CSV_PATH)
    years = df["Year"].astype(int).tolist()
    series = []

    for column in df.columns[1:]:
        if column == "United Kingdom":
            kind = "uk"
        elif column == "OECD average":
            kind = "oecd"
        elif column == "Global average":
            kind = "global"
        else:
            kind = "other"

        values = [
            None if pd.isna(value) else round(float(value), 4)
            for value in df[column].tolist()
        ]
        series.append(
            {
                "name": column,
                "kind": kind,
                "values": values,
            }
        )

    return {"years": years, "series": series}


def main():
    if not DATA_CSV_PATH.exists():
        raise FileNotFoundError(f"Missing {DATA_CSV_PATH}")
    if not LOGO_PATH.exists():
        raise FileNotFoundError(f"Missing {LOGO_PATH}")

    payload = build_payload()
    logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    html = (
        HTML_TEMPLATE.replace("__BR_RED__", BR_RED)
        .replace("__BR_BLUE__", BR_BLUE)
        .replace("__BR_NAVY__", BR_NAVY)
        .replace("__BR_BLACK__", BR_BLACK)
        .replace("__BR_GREY__", BR_GREY)
        .replace("__GRID_GREY__", GRID_GREY)
        .replace("__SECONDARY_LINE__", SECONDARY_LINE)
        .replace("{{", "{")
        .replace("}}", "}")
        .replace("__DATA_PAYLOAD__", json.dumps(payload, separators=(",", ":")))
        .replace("__LOGO_DATA__", logo_b64)
    )

    OUTPUT_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML_PATH.write_text(html)
    print(f"Wrote {OUTPUT_HTML_PATH}")


if __name__ == "__main__":
    main()
