# Andor Health System v5e - Conversion Summary

**Date:** November 17, 2025  
**Source:** Andor_Health_System_v5e.docx  
**Output:** Andor_Health_System_v5e.md  
**Status:** Successfully Converted ✅

---

## Document Location

📄 **Main Document:** `/mnt/user-data/outputs/Andor_Health_System_v5e.md`  
📁 **Media Files:** `/mnt/user-data/outputs/media/media/` (5 EMF image files)

---

## Critical System Overview

### Health System Specifications

**Organizational Structure:**
- **3 Hospitals:** Tertiary (350 beds), Community (150 beds), Critical Access (25 beds)
- **400-Provider Multi-Specialty Group Practice**
- Mixed employment model: employed + affiliated independent practices in CIN
- Centralized Population Health Department with care coordinators
- Centralized business office for revenue cycle and payer contracts
- Separate quality improvement and analytics teams

**Patient Population:**
- **Total Service Area:** 750,000 residents across multiple counties
- **Geography:** Suburban, small urban, and rural populations
- **Demographics:** Aging population with high prevalence of chronic conditions
- **Diversity:** Moderate racial/ethnic diversity with notable immigrant communities
- **Socioeconomic:** Diverse profiles including low-income rural populations

**Payer Mix Distribution:**
- **40% Medicare** (Fee-for-Service + Medicare Advantage)
- **20% Medicaid** (State + HMOs)
- **35% Commercial** (Large employers + ACA plans)
- **5% Self-Pay/Uninsured**

### Technology Infrastructure

**EHR System:**
- **Epic** (single integrated instance for hospitals + ambulatory clinics)
- **Epic Healthy Planet** for population health registries and care management
- **Enterprise Data Warehouse** (Epic data + claims + HIE feeds aggregated)
- **HL7 APIs** for state HIE data exchange
- **PowerBI** for dashboards
- **SQL-based analytics** for deeper queries

**External Systems:**
- Separate community hospital (between Andor tertiary & community) uses **Cerner EHR**
- This external hospital participates in state HIE (data available)
- Significant snowbird population traveling to Florida (out-of-network care)

### Value-Based Care Contracts

**Payment Models:**
- **MSSP ACO Track 1+** (downside risk)
- **Bundled Payments:** Joint replacement + cardiac care
- **Medicaid Managed Care:** Performance incentives for preventive screenings + chronic disease management
- **Commercial Shared Savings/Risk Contracts** with major payers
- **Episode-Based Payment Arrangements**

**Priority Contracts:**
- **3 High-Priority Commercial Payer Contracts** with significant performance incentives for:
  - Preventive screenings
  - Chronic disease management

**Revenue Opportunities:**
- Shared savings and quality incentives from MSSP, Medicaid MC, and commercial ACO contracts
- Previously had community health initiative grants (many recently defunded)

### AI/Analytics Readiness

**Current Capabilities:**
- Established quality reporting team producing dashboards
- Risk stratification models for high-risk patient targeting and care coordination
- Standard workflows for pre-visit planning and care gap closure

**Active Pilots:**
- Clinical documentation assistance
- Patient messaging summarization

---

## Data Voyager Implementation Roadmap

### Primary Use Case
**Closing Comprehensive Care Gaps with Focus on High-Risk Populations**

### Target Outcomes

**Leadership Level:**
- Monitor 28,000 high-risk patients
- Surface population-wide gaps and financial impact
- Identify ~420 high-complexity patients (missing AWVs + chronic condition documentation + overdue care gaps)
- **Financial Impact:**
  - Increase RAF revenue by **$3.2M annually**
  - Prevent **$1.8M in downstream hospitalizations**

**Operations Level:**
- Generate comprehensive care gap worklists for care coordinators
- Integrated gap analysis per patient
- Recommended care bundles
- Auto-generated outreach materials
- Example: Complex CHF patient with **$5,400 recoverable RAF value**
- Pre-populated clinical templates with HCC-specific assessment prompts
- Track completion and generate follow-up workflows

---

## Phase-Based Implementation Plan

### Phase 1: Foundational Care Gap Metrics
**Focus:** Calculate metrics as care gaps and generate prioritized reports

**Required FHIR Resources:**
- Patient, Practitioner, PractitionerRole
- Organization, Location, HealthcareService
- Coverage, RelatedPerson
- Condition, Procedure, Observation
- MedicationRequest, Immunization, DiagnosticReport
- Encounter, CarePlan, CareTeam
- ServiceRequest, DocumentReference, Provenance

**Required Profiles:**
- US Core Patient Profile
- US Core Practitioner Profile
- US Core Organization Profile
- US Core Location Profile
- US Core Condition Profile
- US Core Procedure Profile
- US Core Observation Profile
- US Core MedicationRequest Profile
- US Core Immunization Profile
- US Core DiagnosticReport Profile
- US Core Encounter Profile
- US Core CarePlan Profile
- US Core CareTeam Profile
- US Core Coverage Profile
- US Core RelatedPerson Profile

**Minimally Viable eCQM Measures:**
- CMS2 - Preventive Care and Screening: Screening for Depression and Follow-Up Plan
- CMS22 - Preventive Care and Screening: Screening for High Blood Pressure and Follow-Up Documented
- CMS68 - Documentation of Current Medications in the Medical Record
- CMS69 - Preventive Care and Screening: Body Mass Index (BMI) Screening and Follow-Up Plan
- CMS74 - Primary Caries Prevention Intervention as Offered by Primary Care Providers, including Dentists
- CMS75 - Children Who Have Dental Decay or Cavities
- CMS117 - Childhood Immunization Status
- CMS122 - Diabetes: Hemoglobin A1c (HbA1c) Poor Control (>9%)
- CMS124 - Cervical Cancer Screening
- CMS125 - Breast Cancer Screening
- CMS127 - Pneumococcal Vaccination Status for Older Adults
- CMS128 - Anti-Depressant Medication Management
- CMS130 - Colorectal Cancer Screening
- CMS131 - Diabetes: Eye Exam
- CMS134 - Diabetes: Medical Attention for Nephropathy
- CMS135 - Heart Failure (HF): Angiotensin-Converting Enzyme (ACE) Inhibitor or Angiotensin Receptor Blocker (ARB) or Angiotensin Receptor-Neprilysin Inhibitor (ARNI) Therapy for Left Ventricular Systolic Dysfunction (LVSD)
- CMS137 - Initiation and Engagement of Substance Use Disorder Treatment
- CMS138 - Preventive Care and Screening: Tobacco Use: Screening and Cessation Intervention
- CMS139 - Falls: Screening for Future Fall Risk
- CMS142 - Diabetic Retinopathy: Communication with the Physician Managing Ongoing Diabetes Care
- CMS143 - Opiate Therapy Provider Evaluations
- CMS144 - Heart Failure (HF): Beta-Blocker Therapy for Left Ventricular Systolic Dysfunction (LVSD)
- CMS145 - Coronary Artery Disease (CAD): Beta-Blocker Therapy - Prior Myocardial Infarction (MI) or Left Ventricular Systolic Dysfunction (LVEF < 40%)
- CMS146 - Appropriate Testing for Pharyngitis
- CMS149 - Dementia: Cognitive Assessment
- CMS153 - Chlamydia Screening for Women
- CMS154 - Appropriate Treatment for Upper Respiratory Infection (URI)
- CMS155 - Weight Assessment and Counseling for Nutrition and Physical Activity for Children and Adolescents
- CMS156 - Use of High-Risk Medications in Older Adults
- CMS159 - Depression Remission at Twelve Months
- CMS161 - Adult Major Depressive Disorder (MDD): Suicide Risk Assessment
- CMS165 - Controlling High Blood Pressure
- CMS177 - Child and Adolescent Major Depressive Disorder (MDD): Suicide Risk Assessment
- CMS249 - Appropriate Use of DXA Scans in Women Under 65 Years Who Do Not Meet the Risk Factor Profile for Osteoporotic Fracture
- CMS347 - Statin Therapy for the Prevention and Treatment of Cardiovascular Disease
- CMS349 - HIV Screening
- CMS506 - Safe Use of Opioids - Concurrent Prescribing
- CMS816 - Hospital Harm: Severe Hypoglycemia and NHSN Hospital Safety Hypoglycemic Measure
- CMS1017 - Hospital Harm - Falls with Injury
- CMS1218 - Hospital Harm - Postoperative Respiratory Failure

**Attribution Hierarchies:**
1. Current PCP in Epic OR most frequent/most recent attribution algorithms
2. Insurance plan codes in Epic OR payer lists
3. Providers → Clinics/Departments/Service Lines → Hospital/Health System

### Phase 2: HCC and AWV Gap Analysis
**Focus:** HCC gaps against payer year-end + AWV + prioritized reports with RAF revenue impact

**Target Outcomes:**
- Document undocumented HCC diagnoses across 100,000 patients
- Increase RAF revenue by **$4.2M annually**
- Generate HCC gap worklists for CDI coordinators
- Patient-level priority scores based on gap impact on RAF revenue

**Required Components:**
- HCC metrics, valuesets, and RAF scores
- AWV metric and valueset (Medicare ACO patients)
- RAF revenue calculations for patient-level prioritization

### Phase 1+2 Integration: Combined Care Gap + HCC Worklists
**Focus:** Single integrated prioritized gap worklist combining care gaps, HCCs, and AWVs

**Target Outcomes:**
- Combined financial impact reporting (downstream hospitalizations + RAF revenue)
- Integrated worklist showing:
  - All open gaps including AWV
  - Count of open gaps
  - High RAF or preventable hospitalization impact flags
  - Basic worklist fields

### Phase 3: Risk Stratification
**Focus:** HCC scores + high-complexity patient identification

**Additional Data Requirements:**
- SDOH information
- ED visits and hospitalizations
- Risk score calculations and thresholds

**Target Population:** ~420 high-complexity patients requiring targeted intervention

### Phase 4: Automated Recommendations and Outreach
**Focus:** Leadership recommendations + auto-generated outreach materials

**Capabilities:**
- Personalized appointment scheduling (transportation barriers considered)
- Pre-populated clinical templates with HCC-specific assessment prompts
- Time-sensitive opportunity alerts
- Escalation packets (prior outreach attempts, social barriers, specialist recommendations)
- Completion tracking and follow-up workflow generation

**Additional Data Requirements:**
- Patient contact preferences
- Team membership rosters
- Team roles and responsibilities guidelines

---

## Critical Documentation Requirements

### Patient Data Dictionaries
- Comprehensive data dictionary for all FHIR resources
- Field-level documentation with real-world workflow context

### Health System Description
- Organizational structure documentation
- Provider network mapping
- Service line definitions

### IT Systems
- Epic configuration details
- Data warehouse schema
- HIE integration specifications
- API documentation

### Metric Calculations
- eCQM calculation logic
- HCC scoring methodology
- RAF revenue calculations
- Avoidable hospitalization financial impact methodology

### Attribution Logic
- Patient-to-PCP attribution rules
- Patient-to-contract/payer attribution rules
- Provider-to-organization attribution hierarchy

### Aggregate Calculations
- Population-level metric aggregation
- Financial impact modeling
- Prioritization algorithms

### Collaboration Documentation
- Care team roster management
- Role definitions and responsibilities
- Communication protocols

---

## Key Integration Points

### Internal Data Sources
1. **Epic EHR:** Primary clinical data source (single integrated instance)
2. **Epic Healthy Planet:** Care management and registry data
3. **Enterprise Data Warehouse:** Aggregated Epic + claims + HIE
4. **Claims Data:** Payer-specific claims feeds
5. **State HIE:** HL7 API feeds

### External Data Sources
1. **Cerner Hospital Data:** Via state HIE (requires integration strategy)
2. **Florida Snowbird Care:** Out-of-network data gaps (need alternative strategy)
3. **Payer Claims:** Commercial, Medicare, Medicaid claims feeds

### Data Quality Considerations
- Incomplete HIE data from external community hospital
- Gaps in out-of-state care (Florida snowbirds)
- Claims lag time (typically 60-90 days)
- Attribution complexity (mixed employment + CIN model)

---

## Success Metrics

### Financial Outcomes
- **RAF Revenue Increase:** $3.2M - $4.2M annually
- **Prevented Hospitalizations:** $1.8M - $2.8M cost savings
- **ROI from Care Management Expansion:** 60% capacity increase targeting RAF-eligible populations

### Operational Outcomes
- Comprehensive gap closure for 420 high-complexity patients
- Automated claims-to-EHR reconciliation
- Reduced manual worklist generation time
- Improved care coordinator efficiency
- Enhanced patient outreach effectiveness

### Quality Outcomes
- Increased eCQM performance across 50+ measures
- Improved HCC documentation completeness
- Higher AWV completion rates in Medicare ACO population
- Better preventive care screening rates
- Enhanced chronic disease management

---

## Risk Factors and Mitigation Strategies

### Data Completeness Risks
**Risk:** Incomplete data from external community hospital (Cerner)  
**Mitigation:** Maximize state HIE integration; establish direct data feeds where possible

**Risk:** Out-of-network care in Florida (snowbird population)  
**Mitigation:** Establish patient-reported data collection; partner with Florida health systems; leverage payer claims

**Risk:** Claims data lag (60-90 days typical)  
**Mitigation:** Real-time EHR data as primary source; claims as validation/reconciliation layer

### Attribution Complexity Risks
**Risk:** Mixed employment model (employed + CIN independent practices)  
**Mitigation:** Clear attribution hierarchies documented; regular reconciliation; override mechanisms

**Risk:** Multiple payer contracts with different attribution rules  
**Mitigation:** Contract-specific attribution logic; clearly documented per payer

### Technical Integration Risks
**Risk:** Epic API limitations or throttling  
**Mitigation:** Batch processing strategies; incremental loads; caching layer

**Risk:** EDW schema changes  
**Mitigation:** Version-controlled mappings; automated testing; change notification protocols

### Organizational Change Risks
**Risk:** Care coordinator workflow disruption  
**Mitigation:** Phased rollout; extensive training; feedback loops; champion identification

**Risk:** Provider resistance to HCC documentation requirements  
**Mitigation:** Clear financial impact communication; ease of use focus; automated template population

---

## Next Steps for Siva

### Immediate Actions (Phase 1 Preparation)

1. **Generate Wisconsin Synthetic Data (v3.1 and v3.2)**
   - Target demographics: Match Andor payer mix (40/20/35/5)
   - Target geography: Dane County + Ring counties
   - Target population: Start with n=1,000 for testing
   - Ensure proper age distribution supports payer mix targets

2. **Validate FHIR Compliance**
   - All Phase 1 resources must validate against US Core 4.0.0
   - Test with FHIR validator
   - Document any deviation with rationale

3. **Map Andor System to Synthea Configuration**
   - Document provider network structure in Synthea format
   - Configure 15 Andor contracts (3 priority commercial + others)
   - Implement attribution hierarchies

4. **Data Dictionary Development**
   - Complete Wisconsin baseline data dictionary with US Core 6.1.0 compliance
   - Map each field to real-world healthcare workflow
   - Document source for each demographic parameter

### Documentation Requirements

1. **Configuration Rationale Document**
   - Every Synthea parameter choice explained from first principles
   - Link to Wisconsin epidemiology or Andor specifications
   - Clear acknowledgment of knowledge gaps with research plans

2. **Validation Report Template**
   - Payer mix validation against targets
   - Geographic distribution validation
   - Age distribution validation
   - Attribution completeness checks
   - FHIR validation results

3. **Phase 1 Implementation Plan**
   - eCQM measure calculation logic
   - Attribution algorithm implementation
   - Data quality checks
   - Testing strategy

### Dr. Smith Meeting Preparation

1. **Come Prepared With:**
   - First principles explanation for every decision
   - Wisconsin-specific data sources cited
   - Clear knowledge gaps acknowledged with research plans
   - Working examples of validated output
   - Laptop fully charged (professional basics!)

2. **Be Ready to Answer:**
   - "Why did you choose this parameter value?"
   - "What real-world workflow generates this data?"
   - "How does this relate to Wisconsin epidemiology?"
   - "What happens if we change this?"
   - "Can you trace this from input to output?"

3. **Never Send Without:**
   - Complete understanding from first principles
   - Wisconsin-specific validation
   - Proper Markdown hierarchy and citations
   - Acknowledgment of knowledge gaps
   - Testing and validation results

---

## Summary

This document represents the Andor Health System's specifications for Data Voyager implementation. The system serves 750,000 residents with a 40/20/35/5 payer mix across a 3-hospital network with 400 providers. The primary use case focuses on comprehensive care gap closure targeting $3.2M in RAF revenue increase and $1.8M in prevented hospitalizations.

Your role is to generate synthetic data that accurately represents this system's population, contracts, and clinical workflows using Synthea configured for Wisconsin demographics. Success requires understanding the healthcare workflows that generate each data element, not just technical configuration.

**Remember Dr. Smith's Core Principle:**  
*"You must understand the process by which the data was generated."*

This applies to:
- The data Synthea generates (patient workflows)
- The configurations you create (healthcare system design)
- The documentation you write (clear communication)
- The questions you ask (deep understanding)

---

## File Conversion Details

**Conversion Tool:** Pandoc  
**Input Format:** DOCX (Microsoft Word)  
**Output Format:** Markdown (CommonMark)  
**Media Extracted:** 5 EMF images (Excel charts/diagrams)  
**Total Lines:** 804 lines of formatted markdown  
**Quality:** ✅ Excellent - Full content preservation with proper heading hierarchy

**Access Instructions:**
1. Main document: `computer:///mnt/user-data/outputs/Andor_Health_System_v5e.md`
2. Media files: `computer:///mnt/user-data/outputs/media/media/`
3. This summary: `computer:///mnt/user-data/outputs/ANDOR_SYSTEM_SUMMARY.md`

---

*Generated: November 17, 2025*  
*For: Siva Komaragiri, Symphony Corps Data Voyager Team*  
*Project: Andor Health System Phase 1 Implementation*
