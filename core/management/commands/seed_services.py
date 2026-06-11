from django.core.management.base import BaseCommand
from django.utils.text import slugify
from services.models import ServiceCategory, Service

SERVICES_DATA = [
    {
        'name': 'Strategy & Investment',
        'slug': 'strategy-investment',
        'icon_class': 'strategy',
        'order': 1,
        'services': [
            {'name': 'Idea Development & Validation', 'short_desc': 'Transform your concept into a viable business idea with structured validation processes and market feedback.', 'body': 'We help entrepreneurs and organisations validate business ideas through structured research, competitor analysis, and market feedback loops. Our process ensures your concept has real-world viability before significant resources are committed.', 'key_deliverables': 'Concept assessment report\nMarket viability analysis\nCompetitor landscape overview\nRisk identification summary', 'order': 1},
            {'name': 'Company / NGO / Trust Registrations', 'short_desc': 'Professional registration services for companies, NGOs, and trusts in Zimbabwe.', 'body': 'We handle end-to-end registration of companies, non-governmental organisations, and trusts with the relevant Zimbabwean regulatory authorities. We ensure compliance from day one.', 'key_deliverables': 'Certificate of incorporation\nConstitution / MoA & AoA drafting\nTax registration\nRegulatory compliance checklist', 'order': 2},
            {'name': 'ZIMRA Returns & Tax Clearances', 'short_desc': 'Timely and accurate ZIMRA tax return submissions and tax clearance certificate procurement.', 'body': 'We manage your ZIMRA obligations — from VAT and PAYE returns to income tax assessments — and obtain tax clearance certificates needed for tenders and contracts.', 'key_deliverables': 'Monthly / quarterly return submissions\nTax clearance certificate\nCompliance calendar\nLiaison with ZIMRA on your behalf', 'order': 3},
            {'name': 'Partnership MOU', 'short_desc': 'Draft and review Memoranda of Understanding to formalise business partnerships.', 'body': 'We draft, review, and facilitate signing of Memoranda of Understanding (MOUs) that clearly define partnership terms, roles, responsibilities, and exit clauses.', 'key_deliverables': 'Tailored MOU document\nNegotiation support\nExecution facilitation', 'order': 4},
            {'name': 'Business Strategy Development', 'short_desc': 'Comprehensive strategic planning to align your organisation for sustainable growth.', 'body': 'We partner with your leadership team to craft a robust, actionable business strategy — defining vision, mission, competitive positioning, and a roadmap for sustainable growth.', 'key_deliverables': 'Strategic plan document (3–5 year)\nSWOT & PESTLE analysis\nKPI framework\nImplementation roadmap', 'order': 5},
            {'name': 'Investment Operations Management', 'short_desc': 'Hands-on management support for investment vehicles and operational excellence.', 'body': 'We provide governance structures, reporting frameworks, and operational oversight for investment entities, helping investors maximise returns and minimise risk.', 'key_deliverables': 'Investment policy statement\nReporting dashboard\nGovernance framework\nQuarterly performance reviews', 'order': 6},
            {'name': 'Business Turnaround & Restructuring', 'short_desc': 'Restore profitability and operational stability for struggling businesses.', 'body': 'We diagnose root causes of underperformance and design turnaround strategies covering financial restructuring, operational efficiency, and organisational redesign.', 'key_deliverables': 'Diagnostic assessment report\nTurnaround action plan\nCash-flow stabilisation strategy\nStakeholder communication plan', 'order': 7},
            {'name': 'Market Entry & Expansion Strategy', 'short_desc': 'Navigate new markets confidently with data-driven entry and expansion strategies.', 'body': 'Whether entering the Zimbabwean market or expanding regionally, we provide intelligence-driven strategies covering regulatory landscape, channel selection, pricing, and risk mitigation.', 'key_deliverables': 'Market entry report\nCompetitor analysis\nGo-to-market plan\nRegulatory compliance checklist', 'order': 8},
            {'name': 'Investment Appraisal & Due Diligence', 'short_desc': 'Independent financial and operational due diligence for investment decisions.', 'body': 'We conduct thorough due diligence on acquisition targets, joint ventures, and investment opportunities — giving investors a clear picture of risk and opportunity before committing capital.', 'key_deliverables': 'Due diligence report\nFinancial health assessment\nLegal & compliance risk review\nInvestment recommendation memo', 'order': 9},
            {'name': 'Strategic Planning Workshops', 'short_desc': 'Facilitated workshops to align leadership teams around vision, strategy, and priorities.', 'body': 'We design and facilitate multi-day strategic planning workshops for boards, executive teams, and leadership groups — turning diverse perspectives into a unified strategic direction.', 'key_deliverables': 'Workshop design & facilitation\nConsolidated strategic outputs\nAction plan with owners and timelines\nFollow-up coaching sessions', 'order': 10},
            {'name': 'Operational Efficiency Reviews', 'short_desc': 'Identify and eliminate operational bottlenecks to boost productivity and reduce costs.', 'body': 'We map your business processes, identify inefficiencies, and recommend practical improvements — from workflow redesign to technology adoption — that deliver measurable cost and time savings.', 'key_deliverables': 'Process mapping report\nEfficiency gap analysis\nImprovement recommendations\nImplementation support', 'order': 11},
        ],
    },
    {
        'name': 'Projects & Feasibility',
        'slug': 'projects-feasibility',
        'icon_class': 'projects',
        'order': 2,
        'services': [
            {'name': 'Market Feasibility Studies', 'short_desc': 'Evidence-based market analysis to determine the viability of your product or service.', 'body': 'We assess market size, demand dynamics, competition, and consumer behaviour to produce a comprehensive feasibility study that informs go/no-go decisions.', 'key_deliverables': 'Market size & segmentation analysis\nDemand forecasting\nCompetitive landscape\nFeasibility verdict and recommendations', 'order': 1},
            {'name': 'Project Feasibility Studies', 'short_desc': 'Technical, financial, and operational feasibility assessment for project proposals.', 'body': 'Our project feasibility studies evaluate technical viability, financial projections, environmental and social impact, and implementation risk — giving funders and decision-makers the confidence to proceed.', 'key_deliverables': 'Technical feasibility assessment\nFinancial modelling & sensitivity analysis\nRisk matrix\nFeasibility report', 'order': 2},
            {'name': 'Business Plans & Proposals', 'short_desc': 'Investor-ready business plans and funding proposals that open doors.', 'body': 'We develop detailed, professionally written business plans and funding proposals tailored to the requirements of banks, investors, development finance institutions, and grant bodies.', 'key_deliverables': 'Executive summary\nFull business plan document\nFinancial projections (3–5 years)\nPitch deck (if required)', 'order': 3},
            {'name': 'Baseline Surveys & Market Research', 'short_desc': 'Rigorous data collection and analysis to establish baseline indicators for projects.', 'body': 'We design and conduct baseline surveys, focus group discussions, and key informant interviews to generate reliable data that guides programme design and measures future impact.', 'key_deliverables': 'Survey instrument design\nData collection & cleaning\nStatistical analysis\nBaseline report with recommendations', 'order': 4},
            {'name': 'Project Design & Logical Frameworks', 'short_desc': 'Design robust, results-oriented projects using the logical framework approach.', 'body': 'We work with development organisations and NGOs to design projects using the logical framework methodology — defining objectives, outputs, outcomes, indicators, and assumptions in a coherent structure.', 'key_deliverables': 'Log frame matrix\nTheory of change\nM&E framework\nProject implementation plan', 'order': 5},
            {'name': 'Financial Modeling & Projections', 'short_desc': 'Dynamic financial models to support decision-making, fundraising, and planning.', 'body': 'We build bespoke financial models for businesses, projects, and investment vehicles — covering revenue projections, cost structures, cash flow, break-even analysis, and scenario modelling.', 'key_deliverables': 'Excel / Google Sheets financial model\nThree-statement model (P&L, balance sheet, cash flow)\nScenario analysis\nExplanatory notes', 'order': 6},
        ],
    },
    {
        'name': 'Research & Funding',
        'slug': 'research-funding',
        'icon_class': 'research',
        'order': 3,
        'services': [
            {'name': 'Funding Proposal Writing', 'short_desc': 'Compelling grant and funding proposals that secure resources for your mission.', 'body': 'We write high-quality funding proposals for NGOs, trusts, and social enterprises targeting foundations, bilateral donors, UN agencies, and impact investors — tailored to each funder\'s priorities and requirements.', 'key_deliverables': 'Proposal narrative\nBudget and budget justification\nLogframe and results framework\nSubmission support', 'order': 1},
            {'name': 'Research & Data Collection', 'short_desc': 'Primary and secondary research services to generate actionable insights.', 'body': 'We conduct qualitative and quantitative research including surveys, interviews, focus groups, desk reviews, and literature syntheses — delivering insights that drive strategy, policy, and programme design.', 'key_deliverables': 'Research design & methodology\nData collection instruments\nField data collection management\nResearch report with findings and recommendations', 'order': 2},
            {'name': 'Grant Identification & Application Support', 'short_desc': 'Find the right funding opportunities and navigate the application process.', 'body': 'We scan the funding landscape to identify grants and calls-for-proposals that match your organisation\'s mandate, then support you through the application process — from concept note to full proposal.', 'key_deliverables': 'Funding opportunity mapping report\nConcept note development\nFull proposal writing\nApplication submission support', 'order': 3},
            {'name': 'Impact Assessment Reports', 'short_desc': 'Rigorous evaluation of programme outcomes and social impact.', 'body': 'We design and conduct impact assessments for development programmes, social enterprises, and CSR initiatives — measuring what changed for whom, by how much, and why, using mixed methods approaches.', 'key_deliverables': 'Assessment design & methodology\nData collection & analysis\nImpact assessment report\nLessons learned and recommendations', 'order': 4},
            {'name': 'Stakeholder Analysis', 'short_desc': 'Map and understand stakeholders to enhance project design and engagement strategies.', 'body': 'We conduct systematic stakeholder analyses to identify key actors, their interests, influence, and relationships — informing communication strategies, partnership approaches, and risk management.', 'key_deliverables': 'Stakeholder mapping matrix\nPower/interest analysis\nEngagement strategy recommendations\nStakeholder register', 'order': 5},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed services catalogue from the GrowthMaster spec'

    def handle(self, *args, **options):
        for cat_data in SERVICES_DATA:
            cat, created = ServiceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'icon_class': cat_data['icon_class'],
                    'order': cat_data['order'],
                },
            )
            if not created:
                cat.name = cat_data['name']
                cat.order = cat_data['order']
                cat.save()

            for svc_data in cat_data['services']:
                slug = slugify(svc_data['name'])
                svc, _ = Service.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'category': cat,
                        'name': svc_data['name'],
                        'short_desc': svc_data['short_desc'],
                        'body': svc_data['body'],
                        'key_deliverables': svc_data.get('key_deliverables', ''),
                        'order': svc_data['order'],
                    },
                )

        self.stdout.write(self.style.SUCCESS('Services catalogue seeded successfully.'))
