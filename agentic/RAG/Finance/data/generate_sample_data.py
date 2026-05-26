"""
Synthetic financial PDF generator for the ICAN GenAI workshop.

Produces 5 realistic-looking (but FICTIONAL) PDFs that the workshop notebooks
reference. Data is internally consistent so the chunking, knowledge graph,
year-over-year, and agentic notebooks all demonstrate cleanly.

Run from the repo root or from this folder:

    python generate_sample_data.py

Output:
    annual_reports/nmb_bank_annual_report_2023.pdf
    annual_reports/nmb_bank_annual_report_2022.pdf
    annual_reports/nepal_telecom_annual_report_2023.pdf
    financial_statements/nmb_bank_financials_2023.pdf
    financial_statements/nepal_telecom_financials_2023.pdf
"""

from __future__ import annotations
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
)

HERE = Path(__file__).resolve().parent
AR_DIR = HERE / "annual_reports"
FS_DIR = HERE / "financial_statements"
AR_DIR.mkdir(exist_ok=True)
FS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Shared styles
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "title", parent=styles["Title"], fontSize=22, leading=26, spaceAfter=18,
    textColor=colors.HexColor("#1A4F8B"),
)
h1 = ParagraphStyle(
    "h1", parent=styles["Heading1"], fontSize=15, leading=20, spaceBefore=14,
    spaceAfter=8, textColor=colors.HexColor("#1A4F8B"),
)
h2 = ParagraphStyle(
    "h2", parent=styles["Heading2"], fontSize=12, leading=16, spaceBefore=10,
    spaceAfter=4, textColor=colors.HexColor("#2C3E50"),
)
body = ParagraphStyle(
    "body", parent=styles["BodyText"], fontSize=10.5, leading=14.5,
    spaceAfter=6, alignment=4,  # justify
)
small = ParagraphStyle(
    "small", parent=styles["BodyText"], fontSize=9, leading=12, spaceAfter=4,
)


def _table(data, col_widths=None, header_bg="#1A4F8B"):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BDC3C7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F4F7FA")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def _para(text, style=body):
    return Paragraph(text, style)


def _spacer(h=0.4):
    return Spacer(1, h * cm)


def _build_pdf(filename: Path, story: list):
    doc = SimpleDocTemplate(
        str(filename), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=filename.stem,
    )
    doc.build(story)
    print(f"  Wrote {filename.relative_to(HERE.parent)}")


# ===========================================================================
# NMB BANK ANNUAL REPORT — FY2023
# ===========================================================================
def build_nmb_2023():
    story = []
    story += [
        _para("NMB Bank Limited", title_style),
        _para("Annual Report — Fiscal Year 2022/23 (FY2023)", h1),
        _para(
            "Registered Office: Babarmahal, Kathmandu, Nepal &nbsp;|&nbsp; "
            "Company Registration No.: 25478/064/065 &nbsp;|&nbsp; "
            "Listed on: Nepal Stock Exchange (NEPSE) — Symbol: NMB",
            small,
        ),
        _para(
            "This is a synthetic document created for the ICAN GenAI training "
            "workshop. All figures, names, and events are fictional and used "
            "only for educational demonstration of RAG and Knowledge Graph "
            "techniques.",
            small,
        ),
        _spacer(),
        _para("Chairperson's Statement", h1),
        _para(
            "On behalf of the Board of Directors, I am pleased to present the "
            "Annual Report of NMB Bank Limited for the fiscal year 2022/23. "
            "Despite a challenging macroeconomic environment characterised by "
            "tightening liquidity and elevated interest rates, NMB Bank "
            "delivered another year of resilient performance. Net profit grew "
            "by 9.8 percent year-on-year, total deposits crossed NPR 250 "
            "billion, and our capital adequacy ratio remained well above the "
            "regulatory minimum at 13.2 percent.",
        ),
        _para(
            "During the year, the Bank continued to expand its branch and "
            "digital footprint, opening 14 new branches across the Karnali and "
            "Sudurpaschim provinces. We also completed the acquisition of a "
            "majority stake in NMB Microfinance Bittiya Sanstha, taking our "
            "ownership to 70.0 percent, and re-affirmed our 51.0 percent "
            "stake in NMB Capital Limited.",
        ),
        _para("— Ram Bahadur Khatri, Chairperson", small),
        _spacer(),

        _para("Board of Directors (As at Ashadh 31, 2080 / 15 July 2023)", h1),
        _table([
            ["Name", "Designation", "Appointed"],
            ["Ram Bahadur Khatri", "Chairperson", "2018"],
            ["Sunita Sharma", "Director (Independent)", "2020"],
            ["Pradeep K. Joshi", "Director", "2019"],
            ["Anjali Pradhan", "Director (Independent)", "2021"],
            ["Bibek Rana", "Director", "2022"],
            ["Sushil Bhatta", "Chief Executive Officer", "2017"],
            ["Manish Timalsina", "Chief Financial Officer", "2019"],
        ], col_widths=[6 * cm, 6 * cm, 3 * cm]),
        _spacer(),

        _para("Financial Highlights — FY2023 (NPR in Millions)", h1),
        _table([
            ["Metric", "FY2023", "FY2022", "Change %"],
            ["Total Assets", "298,420", "274,310", "+8.79%"],
            ["Total Deposits", "251,640", "230,180", "+9.32%"],
            ["Loans and Advances", "212,890", "197,420", "+7.84%"],
            ["Total Equity", "32,150", "29,640", "+8.47%"],
            ["Net Interest Income", "11,820", "10,440", "+13.22%"],
            ["Operating Income", "16,540", "14,920", "+10.86%"],
            ["Net Profit", "4,184", "3,810", "+9.82%"],
            ["Capital Adequacy Ratio (CAR)", "13.20%", "12.85%", "+35 bps"],
            ["Non-Performing Loans (NPL)", "2.41%", "2.18%", "+23 bps"],
            ["Return on Equity (ROE)", "13.45%", "13.10%", "+35 bps"],
            ["Earnings Per Share (NPR)", "23.40", "22.15", "+5.64%"],
        ], col_widths=[6 * cm, 3 * cm, 3 * cm, 3 * cm]),
        _spacer(),
        PageBreak(),

        _para("Management Discussion and Analysis (MD&A)", h1),
        _para("Operating Environment", h2),
        _para(
            "The Nepalese banking sector navigated a difficult year with the "
            "Nepal Rastra Bank (NRB) maintaining a tight monetary stance to "
            "control imports and stabilise foreign exchange reserves. The "
            "policy rate was held at 7.0 percent for most of the year, and "
            "the cash reserve ratio (CRR) was retained at 4.0 percent. "
            "Despite these headwinds, NMB Bank maintained healthy net interest "
            "margins of 4.3 percent compared to 4.1 percent in FY2022."
        ),
        _para("Deposit and Lending Growth", h2),
        _para(
            "Total deposits grew by NPR 21.46 billion to reach NPR 251.64 "
            "billion. Retail deposits contributed 62 percent of the deposit "
            "base, demonstrating the stickiness of the Bank's retail "
            "franchise. The loans-to-deposits ratio stood at 84.6 percent, "
            "well within the regulatory ceiling of 90 percent. Lending to the "
            "agriculture, hydropower, and SME sectors increased by 11.2 "
            "percent, 14.7 percent, and 9.4 percent respectively."
        ),
        _para("Asset Quality", h2),
        _para(
            "The Non-Performing Loan ratio rose marginally to 2.41 percent "
            "from 2.18 percent the previous year, primarily attributable to "
            "stress in the tourism and trading portfolios in the first half "
            "of the fiscal year. Provision coverage was strengthened to 138 "
            "percent and write-offs of NPR 412 million were undertaken in the "
            "second half. We expect NPL ratios to normalise to under 2.20 "
            "percent by Q2 FY2024."
        ),
        _para("Capital and Liquidity", h2),
        _para(
            "Capital Adequacy Ratio improved to 13.20 percent (FY2022: 12.85 "
            "percent), comfortably above the Basel III minimum of 11.0 percent "
            "set by Nepal Rastra Bank. Tier 1 capital ratio was 10.85 percent. "
            "The Bank issued NPR 2.0 billion of subordinated debentures in "
            "Magh 2079 to support Tier 2 capital."
        ),
        _spacer(),

        _para("Subsidiaries and Associates", h1),
        _table([
            ["Subsidiary / Associate", "Ownership %", "Principal Activity"],
            ["NMB Capital Limited", "51.0%", "Merchant banking, IPO advisory"],
            ["NMB Microfinance Bittiya Sanstha", "70.0%", "Microfinance services"],
            ["NMB Insurance Brokers Pvt. Ltd.", "100.0%", "Insurance brokerage"],
        ], col_widths=[7 * cm, 3 * cm, 6 * cm]),
        _spacer(),
        PageBreak(),

        _para("Risk Management — Key Risk Factors", h1),
        _para(
            "1. <b>Credit Risk:</b> Concentration in the hydropower and real "
            "estate sectors represents 28 percent of total loan exposure. A "
            "sustained decline in property prices or hydropower tariff "
            "compression would directly affect asset quality.",
        ),
        _para(
            "2. <b>Liquidity Risk:</b> Tightness in interbank markets during "
            "Q2 FY2023 caused short-term funding costs to spike by 180 basis "
            "points. The Bank has since increased its high-quality liquid "
            "asset buffer to 22 percent of total deposits.",
        ),
        _para(
            "3. <b>Foreign Exchange Risk:</b> Nepal's dependence on imports "
            "and remittance inflows exposes the Bank to indirect FX risk. "
            "Direct FX exposure is limited to NPR 4.2 billion in approved "
            "open positions.",
        ),
        _para(
            "4. <b>Cyber and Operational Risk:</b> The Bank invested NPR 380 "
            "million in cybersecurity and core banking upgrades during the "
            "year. Two minor phishing incidents were detected and contained "
            "in Falgun 2079 with no customer data loss.",
        ),
        _para(
            "5. <b>Regulatory Risk:</b> Anticipated changes to working "
            "capital lending guidelines and the proposed Banks and Financial "
            "Institutions Act (BAFIA) amendments may affect lending margins "
            "in FY2024.",
        ),
        _spacer(),

        _para("Independent Auditor's Report", h1),
        _para(
            "To the Shareholders of NMB Bank Limited:", h2,
        ),
        _para(
            "We have audited the financial statements of NMB Bank Limited "
            "(\"the Bank\") for the year ended Ashadh 31, 2080 (15 July 2023). "
            "In our opinion, the financial statements give a true and fair "
            "view of the financial position of the Bank as at the year end, "
            "and of its financial performance and cash flows for the year then "
            "ended in accordance with Nepal Financial Reporting Standards "
            "(NFRS) and the Bank and Financial Institutions Act, 2073.",
        ),
        _para("Key Audit Matters", h2),
        _para(
            "<b>(a) Expected Credit Loss on Loans and Advances:</b> The Bank's "
            "loans and advances of NPR 212,890 million are net of expected "
            "credit loss provisions of NPR 5,142 million. The determination "
            "of provisions involves significant management judgement, "
            "particularly with respect to staging of loans and forward-looking "
            "macroeconomic adjustments.",
        ),
        _para(
            "<b>(b) IT Systems and Controls:</b> The Bank's reliance on "
            "automated processes and IT controls is significant. We tested "
            "the design and operating effectiveness of general IT controls "
            "and key application controls, including the new core banking "
            "release deployed in Mangsir 2079.",
        ),
        _para(
            "Audited by: <b>Deloitte Haskins &amp; Sells</b>, Chartered "
            "Accountants. Registered Office: Babarmahal, Kathmandu. "
            "Audit partner: CA Rajesh Pradhan, ICAN Membership No. 4421. "
            "Audit report dated: Kartik 12, 2080.",
            small,
        ),
        _spacer(),
        PageBreak(),

        _para("Corporate Governance", h1),
        _para(
            "The Board of Directors met 14 times during the fiscal year. The "
            "Audit Committee, chaired by Ms. Sunita Sharma (Independent "
            "Director), met 8 times. The Risk Management Committee met 6 "
            "times and reviewed the Bank's risk appetite framework in "
            "Chaitra 2079. Director attendance averaged 92 percent across "
            "all meetings.",
        ),
        _para(
            "NMB Bank complies with the Corporate Governance Directives "
            "issued by Nepal Rastra Bank and the Securities Board of Nepal "
            "(SEBON). The Bank's Code of Conduct was updated in Bhadra 2079 "
            "to incorporate enhanced whistleblower protections.",
        ),
        _spacer(),

        _para("Dividend and Capital Distribution", h1),
        _para(
            "The Board has recommended a cash dividend of 11.0 percent and a "
            "bonus share issue of 4.5 percent on paid-up capital, subject to "
            "approval at the Annual General Meeting. Total distribution "
            "equates to NPR 2,418 million, representing 57.8 percent of net "
            "profit for FY2023.",
        ),
    ]
    _build_pdf(AR_DIR / "nmb_bank_annual_report_2023.pdf", story)


# ===========================================================================
# NMB BANK ANNUAL REPORT — FY2022 (prior year, similar structure)
# ===========================================================================
def build_nmb_2022():
    story = []
    story += [
        _para("NMB Bank Limited", title_style),
        _para("Annual Report — Fiscal Year 2021/22 (FY2022)", h1),
        _para(
            "Registered Office: Babarmahal, Kathmandu, Nepal &nbsp;|&nbsp; "
            "Company Registration No.: 25478/064/065 &nbsp;|&nbsp; "
            "Listed on: Nepal Stock Exchange (NEPSE) — Symbol: NMB",
            small,
        ),
        _para(
            "Synthetic document for the ICAN GenAI workshop. All figures and "
            "names are fictional.", small,
        ),
        _spacer(),

        _para("Chairperson's Statement", h1),
        _para(
            "Fiscal year 2021/22 was a year of recovery and consolidation for "
            "NMB Bank. As the economy rebounded from the COVID-19 disruptions, "
            "the Bank registered net profit growth of 11.4 percent, with "
            "total assets crossing NPR 270 billion for the first time. The "
            "Bank opened 9 new branches during the year and completed the "
            "integration of its earlier acquisition of Kanchan Development "
            "Bank.",
        ),
        _para("— Ram Bahadur Khatri, Chairperson", small),
        _spacer(),

        _para("Board of Directors (As at Ashadh 31, 2079 / 16 July 2022)", h1),
        _table([
            ["Name", "Designation", "Appointed"],
            ["Ram Bahadur Khatri", "Chairperson", "2018"],
            ["Sunita Sharma", "Director (Independent)", "2020"],
            ["Pradeep K. Joshi", "Director", "2019"],
            ["Kamal Adhikari", "Director (Independent)", "2018"],
            ["Sushil Bhatta", "Chief Executive Officer", "2017"],
            ["Manish Timalsina", "Chief Financial Officer", "2019"],
        ], col_widths=[6 * cm, 6 * cm, 3 * cm]),
        _spacer(),

        _para("Financial Highlights — FY2022 (NPR in Millions)", h1),
        _table([
            ["Metric", "FY2022", "FY2021", "Change %"],
            ["Total Assets", "274,310", "248,140", "+10.55%"],
            ["Total Deposits", "230,180", "208,940", "+10.17%"],
            ["Loans and Advances", "197,420", "176,260", "+12.01%"],
            ["Total Equity", "29,640", "27,180", "+9.05%"],
            ["Net Interest Income", "10,440", "9,310", "+12.14%"],
            ["Operating Income", "14,920", "13,420", "+11.18%"],
            ["Net Profit", "3,810", "3,420", "+11.40%"],
            ["Capital Adequacy Ratio (CAR)", "12.85%", "13.05%", "-20 bps"],
            ["Non-Performing Loans (NPL)", "2.18%", "1.94%", "+24 bps"],
            ["Return on Equity (ROE)", "13.10%", "12.84%", "+26 bps"],
            ["Earnings Per Share (NPR)", "22.15", "21.06", "+5.18%"],
        ], col_widths=[6 * cm, 3 * cm, 3 * cm, 3 * cm]),
        _spacer(),
        PageBreak(),

        _para("Management Discussion and Analysis (MD&A)", h1),
        _para("Operating Environment", h2),
        _para(
            "FY2021/22 was characterised by the gradual normalisation of "
            "economic activity post-pandemic, combined with rising inflation "
            "driven by global commodity prices. Nepal Rastra Bank raised the "
            "policy rate from 5.0 percent to 7.0 percent during the year, "
            "compressing margins across the banking system.",
        ),
        _para("Deposit and Lending Growth", h2),
        _para(
            "The Bank achieved deposit growth of 10.2 percent and credit "
            "growth of 12.0 percent. Lending to the hydropower sector grew "
            "by 18 percent as several large infrastructure projects reached "
            "financial closure. The loans-to-deposits ratio increased to "
            "85.8 percent at year end.",
        ),
        _para("Asset Quality", h2),
        _para(
            "NPL ratio rose to 2.18 percent (FY2021: 1.94 percent) reflecting "
            "stress in tourism and aviation portfolios. The Bank made "
            "additional provisions of NPR 285 million during the year.",
        ),
        _spacer(),

        _para("Subsidiaries and Associates", h1),
        _table([
            ["Subsidiary / Associate", "Ownership %", "Principal Activity"],
            ["NMB Capital Limited", "51.0%", "Merchant banking, IPO advisory"],
            ["NMB Microfinance Bittiya Sanstha", "55.0%", "Microfinance services"],
            ["NMB Insurance Brokers Pvt. Ltd.", "100.0%", "Insurance brokerage"],
        ], col_widths=[7 * cm, 3 * cm, 6 * cm]),
        _spacer(),

        _para("Risk Management — Key Risk Factors", h1),
        _para(
            "Principal risks during FY2022 included credit concentration in "
            "the tourism sector (subsequently moderated), liquidity risk from "
            "tighter NRB monetary policy, and operational risk from the "
            "ongoing core banking transition. The Bank's risk appetite was "
            "reviewed by the Risk Management Committee in Poush 2078."
        ),
        _spacer(),

        _para("Independent Auditor's Report", h1),
        _para(
            "We have audited the financial statements of NMB Bank Limited "
            "for the year ended Ashadh 31, 2079 (16 July 2022). The financial "
            "statements give a true and fair view in accordance with NFRS.",
        ),
        _para(
            "Audited by: <b>Deloitte Haskins &amp; Sells</b>, Chartered "
            "Accountants. Audit partner: CA Rajesh Pradhan. Audit report "
            "dated: Kartik 18, 2079.",
            small,
        ),
        _spacer(),

        _para("Dividend and Capital Distribution", h1),
        _para(
            "The Board recommended a cash dividend of 9.5 percent and a bonus "
            "share issue of 5.0 percent for FY2022, representing 56.4 percent "
            "of net profit.",
        ),
    ]
    _build_pdf(AR_DIR / "nmb_bank_annual_report_2022.pdf", story)


# ===========================================================================
# NEPAL TELECOM ANNUAL REPORT — FY2023
# ===========================================================================
def build_ntc_2023():
    story = []
    story += [
        _para("Nepal Doorsanchar Company Limited (Nepal Telecom)", title_style),
        _para("Annual Report — Fiscal Year 2022/23 (FY2023)", h1),
        _para(
            "Registered Office: Bhadrakali Plaza, Kathmandu, Nepal &nbsp;|&nbsp; "
            "Listed on: Nepal Stock Exchange (NEPSE) — Symbol: NTC &nbsp;|&nbsp; "
            "Government Stake: 91.49 percent",
            small,
        ),
        _para(
            "Synthetic document for the ICAN GenAI workshop. Figures are "
            "fictional and used solely for educational demonstration.",
            small,
        ),
        _spacer(),

        _para("Managing Director's Statement", h1),
        _para(
            "Fiscal year 2022/23 was a transformational year for Nepal Telecom. "
            "We successfully launched commercial 5G services in select urban "
            "areas, expanded our 4G coverage to 78 percent of the population, "
            "and crossed 18 million active mobile subscribers. Despite "
            "intense competitive pressure on voice and data tariffs, the "
            "Company achieved revenue growth of 4.1 percent and a net profit "
            "of NPR 9.86 billion.",
        ),
        _para("— Sangita Pandey, Managing Director", small),
        _spacer(),

        _para("Board of Directors (As at Ashadh 31, 2080 / 15 July 2023)", h1),
        _table([
            ["Name", "Designation", "Appointed"],
            ["Dilli Adhikari", "Chairperson", "2021"],
            ["Sangita Pandey", "Managing Director", "2022"],
            ["Bhojraj Ghimire", "Director (Government Nominee)", "2020"],
            ["Renu Karki", "Director (Independent)", "2021"],
            ["Hari Prasad Neupane", "Director (Government Nominee)", "2019"],
            ["Bikash Shrestha", "Chief Financial Officer", "2020"],
        ], col_widths=[6 * cm, 6 * cm, 3 * cm]),
        _spacer(),

        _para("Financial Highlights — FY2023 (NPR in Millions)", h1),
        _table([
            ["Metric", "FY2023", "FY2022", "Change %"],
            ["Total Assets", "152,840", "146,920", "+4.03%"],
            ["Total Revenue", "47,180", "45,320", "+4.10%"],
            ["Operating Profit", "13,420", "13,180", "+1.82%"],
            ["Net Profit", "9,860", "9,640", "+2.28%"],
            ["Total Equity", "98,140", "92,460", "+6.14%"],
            ["Cash and Bank Balance", "34,820", "32,180", "+8.20%"],
            ["Earnings Per Share (NPR)", "65.73", "64.27", "+2.27%"],
            ["Return on Equity (ROE)", "10.05%", "10.43%", "-38 bps"],
            ["Net Profit Margin", "20.90%", "21.27%", "-37 bps"],
            ["Active Mobile Subscribers (millions)", "18.24", "17.61", "+3.58%"],
        ], col_widths=[6 * cm, 3 * cm, 3 * cm, 3 * cm]),
        _spacer(),
        PageBreak(),

        _para("Management Discussion and Analysis (MD&A)", h1),
        _para("Industry Environment", h2),
        _para(
            "Nepal's telecommunications sector witnessed continued data tariff "
            "compression, with average revenue per user (ARPU) for mobile "
            "data declining by 6 percent year-on-year. The Nepal "
            "Telecommunications Authority (NTA) approved spectrum reallocation "
            "in the 700 MHz band during the year, paving the way for 5G "
            "deployment. Competition from Ncell remained intense.",
        ),
        _para("5G and Network Expansion", h2),
        _para(
            "Nepal Telecom invested NPR 8.4 billion in capital expenditure "
            "during the year, of which NPR 3.2 billion was directed to 5G "
            "infrastructure in Kathmandu, Pokhara and Biratnagar. A further "
            "NPR 2.1 billion was spent on rural 4G coverage expansion, "
            "bringing 4G availability to 78 percent of the population "
            "(FY2022: 71 percent).",
        ),
        _para("Subscriber Base and ARPU", h2),
        _para(
            "Active mobile subscribers grew to 18.24 million (FY2022: 17.61 "
            "million). Postpaid subscribers grew faster at 9.2 percent "
            "compared to 3.5 percent growth in prepaid. Blended mobile ARPU "
            "stood at NPR 198 per month (FY2022: NPR 207).",
        ),
        _spacer(),

        _para("Subsidiaries and Associates", h1),
        _table([
            ["Subsidiary / Associate", "Ownership %", "Principal Activity"],
            ["NT Digital Services Pvt. Ltd.", "100.0%", "Digital payments, cloud services"],
            ["Nepal Satellite Telecom Pvt. Ltd.", "60.0%", "Satellite communications"],
        ], col_widths=[7 * cm, 3 * cm, 6 * cm]),
        _spacer(),
        PageBreak(),

        _para("Risk Management — Key Risk Factors", h1),
        _para(
            "1. <b>Tariff and Competitive Risk:</b> Continued price competition "
            "from Ncell and emerging OTT services threatens voice and SMS "
            "revenues. Voice revenues declined by 11 percent year-on-year.",
        ),
        _para(
            "2. <b>Technology Risk:</b> The 5G rollout requires significant "
            "capital investment ahead of revenue realisation. Payback periods "
            "for 5G are estimated at 5-7 years.",
        ),
        _para(
            "3. <b>Regulatory Risk:</b> The Telecommunications Service Royalty "
            "rate of 4 percent of gross revenue, plus rural telecommunications "
            "development fee of 2 percent, materially affect operating margins. "
            "Any further increase would compress profitability.",
        ),
        _para(
            "4. <b>Cybersecurity Risk:</b> As Nepal's largest "
            "telecommunications operator, the Company is a high-value target "
            "for cyber-attacks. Investment in security operations centre "
            "(SOC) capabilities was increased to NPR 240 million during the "
            "year.",
        ),
        _spacer(),

        _para("Independent Auditor's Report", h1),
        _para(
            "To the Shareholders of Nepal Doorsanchar Company Limited:", h2,
        ),
        _para(
            "We have audited the financial statements of Nepal Doorsanchar "
            "Company Limited for the year ended Ashadh 31, 2080. In our "
            "opinion the financial statements present fairly, in all material "
            "respects, the financial position and performance of the Company "
            "in accordance with NFRS.",
        ),
        _para("Key Audit Matters", h2),
        _para(
            "<b>(a) Revenue Recognition:</b> Telecommunications revenue "
            "comprises multiple performance obligations (voice, data, "
            "interconnect, equipment). The complexity of bundled offerings "
            "requires significant judgement in identifying performance "
            "obligations and allocating transaction prices.",
        ),
        _para(
            "<b>(b) Network Asset Impairment:</b> 3G network assets totaling "
            "NPR 6.4 billion are at risk of accelerated obsolescence given "
            "the 5G rollout. Management performed impairment testing using "
            "discounted cash flow models with a discount rate of 12.5 "
            "percent.",
        ),
        _para(
            "Audited by: <b>BDO Nepal</b>, Chartered Accountants. Audit "
            "partner: CA Pradeep Sharma, ICAN Membership No. 3892. "
            "Audit report dated: Mangsir 6, 2080.", small,
        ),
        _spacer(),

        _para("Dividend and Capital Distribution", h1),
        _para(
            "The Board has recommended a cash dividend of 30.0 percent on "
            "paid-up capital for FY2023, in line with the Government's "
            "expectation as the majority shareholder. Total dividend "
            "distribution amounts to NPR 4.50 billion, representing 45.6 "
            "percent of net profit.",
        ),
    ]
    _build_pdf(AR_DIR / "nepal_telecom_annual_report_2023.pdf", story)


# ===========================================================================
# NMB BANK FINANCIAL STATEMENTS — FY2023
# ===========================================================================
def build_nmb_financials_2023():
    story = []
    story += [
        _para("NMB Bank Limited", title_style),
        _para("Financial Statements — Fiscal Year 2022/23 (FY2023)", h1),
        _para(
            "For the year ended Ashadh 31, 2080 (15 July 2023). All amounts "
            "in NPR Millions unless otherwise stated. Prepared in accordance "
            "with Nepal Financial Reporting Standards (NFRS).", small,
        ),
        _para(
            "Synthetic document for ICAN GenAI workshop. All figures are "
            "fictional and internally consistent for educational use.", small,
        ),
        _spacer(),

        _para("Statement of Financial Position (Balance Sheet)", h1),
        _table([
            ["Particulars", "FY2023", "FY2022"],
            ["ASSETS", "", ""],
            ["Cash and Cash Equivalents", "28,460", "25,180"],
            ["Due from Nepal Rastra Bank", "14,920", "13,640"],
            ["Placements with Banks and FIs", "9,840", "8,720"],
            ["Loans and Advances to Customers", "212,890", "197,420"],
            ["Investment Securities", "28,140", "26,360"],
            ["Property, Plant and Equipment", "2,820", "2,460"],
            ["Intangible Assets", "412", "385"],
            ["Other Assets", "938", "145"],
            ["Total Assets", "298,420", "274,310"],
            ["", "", ""],
            ["LIABILITIES", "", ""],
            ["Due to Banks and FIs", "12,840", "11,260"],
            ["Customer Deposits", "251,640", "230,180"],
            ["Debt Securities Issued", "2,420", "420"],
            ["Other Liabilities (Current)", "16,420", "15,180"],
            ["Provisions", "950", "830"],
            ["Total Liabilities", "284,270", "257,870"],
            ["Deferred Tax Liabilities (Non-Current)", "240", "210"],
            ["", "", ""],
            ["EQUITY", "", ""],
            ["Share Capital", "17,880", "17,200"],
            ["Reserves and Surplus", "14,270", "12,440"],
            ["Total Equity", "32,150", "29,640"],
            ["", "", ""],
            ["Total Liabilities and Equity", "316,660", "287,720"],
        ], col_widths=[9 * cm, 3.5 * cm, 3.5 * cm]),
        _spacer(),
        PageBreak(),

        _para("Statement of Profit or Loss", h1),
        _table([
            ["Particulars", "FY2023", "FY2022"],
            ["Interest Income", "24,180", "21,620"],
            ["Interest Expense", "(12,360)", "(11,180)"],
            ["Net Interest Income", "11,820", "10,440"],
            ["Fees and Commission Income", "3,420", "3,140"],
            ["Fees and Commission Expense", "(480)", "(420)"],
            ["Net Fees and Commission Income", "2,940", "2,720"],
            ["Net Trading Income", "640", "580"],
            ["Other Operating Income", "1,140", "1,180"],
            ["Operating Income", "16,540", "14,920"],
            ["Personnel Expenses", "(3,820)", "(3,440)"],
            ["Operating Expenses", "(3,180)", "(2,920)"],
            ["Depreciation and Amortisation", "(420)", "(380)"],
            ["Impairment Charges on Loans", "(2,840)", "(2,420)"],
            ["Profit Before Tax", "6,280", "5,760"],
            ["Tax Expense", "(2,096)", "(1,950)"],
            ["Net Profit for the Year", "4,184", "3,810"],
            ["", "", ""],
            ["Earnings Per Share (Basic, NPR)", "23.40", "22.15"],
        ], col_widths=[9 * cm, 3.5 * cm, 3.5 * cm]),
        _spacer(),

        _para("Selected Liquidity and Solvency Indicators", h1),
        _table([
            ["Indicator", "FY2023", "FY2022"],
            ["Current Assets (Cash + Due NRB + Placements + ST Loans)", "78,260", "70,440"],
            ["Current Liabilities (Customer Demand Dep. + Due to Banks + Other)", "62,140", "55,820"],
            ["Current Ratio (times)", "1.26", "1.26"],
            ["Total Equity", "32,150", "29,640"],
            ["Total Liabilities", "284,270", "257,870"],
            ["Debt-to-Equity Ratio (times)", "8.84", "8.70"],
            ["Net Profit Margin (Net Profit / Operating Income)", "25.30%", "25.54%"],
            ["Return on Equity (ROE)", "13.45%", "13.10%"],
            ["Return on Assets (ROA)", "1.46%", "1.45%"],
            ["Capital Adequacy Ratio (CAR)", "13.20%", "12.85%"],
        ], col_widths=[9 * cm, 3.5 * cm, 3.5 * cm]),
        _spacer(),
        PageBreak(),

        _para("Notes to the Financial Statements (Selected)", h1),
        _para("Note 1 — Basis of Preparation", h2),
        _para(
            "The financial statements have been prepared in accordance with "
            "Nepal Financial Reporting Standards (NFRS), Bank and Financial "
            "Institutions Act 2073, and applicable directives issued by Nepal "
            "Rastra Bank. The functional currency is the Nepalese Rupee (NPR).",
        ),
        _para("Note 2 — Loans and Advances by Sector", h2),
        _table([
            ["Sector", "FY2023 (NPR M)", "% of Total"],
            ["Hydropower", "42,820", "20.1%"],
            ["Real Estate and Construction", "37,640", "17.7%"],
            ["Manufacturing", "31,140", "14.6%"],
            ["Trading and Services", "29,860", "14.0%"],
            ["Agriculture and Forestry", "21,940", "10.3%"],
            ["SME (Small and Medium Enterprises)", "26,420", "12.4%"],
            ["Personal / Consumer", "16,820", "7.9%"],
            ["Others", "6,250", "2.9%"],
            ["Total Loans and Advances", "212,890", "100.0%"],
        ], col_widths=[7 * cm, 4 * cm, 3 * cm]),
        _spacer(),

        _para("Note 3 — Capital Adequacy", h2),
        _para(
            "The Bank's capital adequacy is calculated in accordance with the "
            "Capital Adequacy Framework 2015 (Updated July 2022) issued by "
            "Nepal Rastra Bank. Tier 1 Capital was NPR 26,420 million "
            "(FY2022: NPR 24,180 million) and Tier 2 Capital was NPR 5,730 "
            "million (FY2022: NPR 3,940 million). Total Risk Weighted "
            "Exposure was NPR 243,560 million.",
        ),
        _para("Note 4 — Related Party Transactions", h2),
        _para(
            "Transactions with subsidiaries during the year included loans "
            "extended to NMB Capital Limited of NPR 420 million, interest "
            "received from NMB Microfinance Bittiya Sanstha of NPR 78 "
            "million, and shared service fees received from NMB Insurance "
            "Brokers Pvt. Ltd. of NPR 12 million.",
        ),
    ]
    _build_pdf(FS_DIR / "nmb_bank_financials_2023.pdf", story)


# ===========================================================================
# NEPAL TELECOM FINANCIAL STATEMENTS — FY2023
# ===========================================================================
def build_ntc_financials_2023():
    story = []
    story += [
        _para("Nepal Doorsanchar Company Limited (Nepal Telecom)", title_style),
        _para("Financial Statements — Fiscal Year 2022/23 (FY2023)", h1),
        _para(
            "For the year ended Ashadh 31, 2080 (15 July 2023). All amounts "
            "in NPR Millions unless otherwise stated. Prepared in accordance "
            "with Nepal Financial Reporting Standards (NFRS).", small,
        ),
        _para(
            "Synthetic document for the ICAN GenAI workshop. All figures are "
            "fictional and used purely for educational demonstration.", small,
        ),
        _spacer(),

        _para("Statement of Financial Position (Balance Sheet)", h1),
        _table([
            ["Particulars", "FY2023", "FY2022"],
            ["ASSETS", "", ""],
            ["Non-Current Assets", "", ""],
            ["Property, Plant and Equipment (Network)", "78,420", "76,180"],
            ["Intangible Assets (Spectrum Licences)", "22,140", "21,460"],
            ["Long-term Investments", "8,420", "7,860"],
            ["Deferred Tax Asset", "1,240", "1,180"],
            ["Total Non-Current Assets", "110,220", "106,680"],
            ["Current Assets", "", ""],
            ["Cash and Bank Balances", "34,820", "32,180"],
            ["Trade Receivables", "5,420", "5,180"],
            ["Inventories (Network Equipment)", "1,840", "1,720"],
            ["Other Current Assets", "540", "1,160"],
            ["Total Current Assets", "42,620", "40,240"],
            ["Total Assets", "152,840", "146,920"],
            ["", "", ""],
            ["EQUITY AND LIABILITIES", "", ""],
            ["EQUITY", "", ""],
            ["Share Capital", "15,000", "15,000"],
            ["Reserves and Retained Earnings", "83,140", "77,460"],
            ["Total Equity", "98,140", "92,460"],
            ["Non-Current Liabilities", "", ""],
            ["Long-term Borrowings", "18,420", "21,180"],
            ["Deferred Income (Subscriber Advances)", "12,640", "11,820"],
            ["Provisions (Decommissioning)", "1,820", "1,640"],
            ["Total Non-Current Liabilities", "32,880", "34,640"],
            ["Current Liabilities", "", ""],
            ["Trade and Other Payables", "11,240", "10,620"],
            ["Short-term Borrowings", "4,820", "3,840"],
            ["Current Tax Liabilities", "2,140", "1,940"],
            ["Accrued Expenses and Provisions", "3,620", "3,420"],
            ["Total Current Liabilities", "21,820", "19,820"],
            ["Total Liabilities", "54,700", "54,460"],
            ["Total Equity and Liabilities", "152,840", "146,920"],
        ], col_widths=[9 * cm, 3.5 * cm, 3.5 * cm]),
        _spacer(),
        PageBreak(),

        _para("Statement of Profit or Loss", h1),
        _table([
            ["Particulars", "FY2023", "FY2022"],
            ["Revenue from Mobile Services", "31,420", "30,180"],
            ["Revenue from Fixed-Line and Broadband", "9,860", "9,420"],
            ["Revenue from Enterprise and Wholesale", "5,900", "5,720"],
            ["Total Revenue", "47,180", "45,320"],
            ["Network Operations and Maintenance", "(11,820)", "(11,180)"],
            ["Interconnect Charges", "(2,640)", "(2,520)"],
            ["Personnel Expenses", "(7,820)", "(7,380)"],
            ["Selling and Marketing", "(2,140)", "(2,040)"],
            ["Other Operating Expenses", "(3,540)", "(3,140)"],
            ["EBITDA", "19,220", "19,060"],
            ["Depreciation and Amortisation", "(5,800)", "(5,880)"],
            ["Operating Profit (EBIT)", "13,420", "13,180"],
            ["Finance Income", "1,840", "1,620"],
            ["Finance Costs", "(1,140)", "(1,260)"],
            ["Profit Before Tax", "14,120", "13,540"],
            ["Tax Expense", "(4,260)", "(3,900)"],
            ["Net Profit for the Year", "9,860", "9,640"],
            ["", "", ""],
            ["Earnings Per Share (Basic, NPR)", "65.73", "64.27"],
        ], col_widths=[9 * cm, 3.5 * cm, 3.5 * cm]),
        _spacer(),

        _para("Selected Liquidity and Solvency Indicators", h1),
        _table([
            ["Indicator", "FY2023", "FY2022"],
            ["Current Assets", "42,620", "40,240"],
            ["Current Liabilities", "21,820", "19,820"],
            ["Current Ratio (times)", "1.95", "2.03"],
            ["Quick Ratio (excl. inventory)", "1.87", "1.94"],
            ["Total Equity", "98,140", "92,460"],
            ["Total Liabilities", "54,700", "54,460"],
            ["Debt-to-Equity Ratio (times)", "0.56", "0.59"],
            ["Net Profit Margin", "20.90%", "21.27%"],
            ["EBITDA Margin", "40.74%", "42.05%"],
            ["Return on Equity (ROE)", "10.05%", "10.43%"],
            ["Return on Assets (ROA)", "6.45%", "6.56%"],
        ], col_widths=[9 * cm, 3.5 * cm, 3.5 * cm]),
        _spacer(),
        PageBreak(),

        _para("Notes to the Financial Statements (Selected)", h1),
        _para("Note 1 — Basis of Preparation", h2),
        _para(
            "These financial statements have been prepared in accordance with "
            "Nepal Financial Reporting Standards (NFRS) and the Company Act "
            "2063. The functional and presentation currency is the Nepalese "
            "Rupee (NPR).",
        ),
        _para("Note 2 — Revenue Disaggregation", h2),
        _table([
            ["Revenue Stream", "FY2023 (NPR M)", "% of Total"],
            ["Mobile Voice", "11,240", "23.8%"],
            ["Mobile Data", "16,420", "34.8%"],
            ["SMS and VAS", "3,760", "8.0%"],
            ["Fixed-Line Voice", "2,180", "4.6%"],
            ["Broadband (FTTH and DSL)", "7,680", "16.3%"],
            ["Enterprise Connectivity", "4,140", "8.8%"],
            ["Wholesale and International", "1,760", "3.7%"],
            ["Total Revenue", "47,180", "100.0%"],
        ], col_widths=[7 * cm, 4 * cm, 3 * cm]),
        _spacer(),

        _para("Note 3 — Property, Plant and Equipment (Network Assets)", h2),
        _para(
            "Network assets comprise base transceiver stations, optical fibre "
            "cable, switching equipment, transmission systems, and "
            "subscriber-end equipment. Capital expenditure during the year "
            "was NPR 8.42 billion, of which NPR 3.20 billion related to 5G "
            "infrastructure. Useful lives for depreciation range from 7 "
            "years (RF equipment) to 20 years (cable network).",
        ),
        _para("Note 4 — Spectrum Licences", h2),
        _para(
            "The Company holds spectrum licences for the 900 MHz, 1800 MHz, "
            "2100 MHz, 2300 MHz, and 700 MHz bands. The newly acquired 700 "
            "MHz licence for 5G services was capitalised at NPR 1.84 billion "
            "during the year and is amortised over the 15-year licence "
            "period.",
        ),
        _para("Note 5 — Related Party Transactions", h2),
        _para(
            "The Government of Nepal holds 91.49 percent of the Company's "
            "share capital. Royalty payments to the Government of NPR 1,887 "
            "million (4 percent of gross revenue) and rural telecommunications "
            "development fees of NPR 943 million (2 percent of gross revenue) "
            "were recognised during the year.",
        ),
    ]
    _build_pdf(FS_DIR / "nepal_telecom_financials_2023.pdf", story)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main():
    print("Generating synthetic financial PDFs for the ICAN GenAI workshop...")
    print(f"Output directory: {HERE}\n")
    build_nmb_2023()
    build_nmb_2022()
    build_ntc_2023()
    build_nmb_financials_2023()
    build_ntc_financials_2023()
    print("\nAll PDFs generated successfully.")
    print("NOTE: All figures and names in these documents are FICTIONAL and "
          "intended only for educational use in the workshop.")


if __name__ == "__main__":
    main()
