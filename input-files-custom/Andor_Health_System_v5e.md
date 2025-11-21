# Contents {#contents .TOC-Heading}

[Goal [1](#goal)](#goal)

[Health System Description [2](#health-system-description)](#health-system-description)

[Organizational Structure and Staffing [2](#organizational-structure-and-staffing)](#organizational-structure-and-staffing)

[Patient Population Demographics [2](#patient-population-demographics)](#patient-population-demographics)

[IT Systems and Data Infrastructure [2](#it-systems-and-data-infrastructure)](#it-systems-and-data-infrastructure)

[Financial Profile and Payment Mix [2](#financial-profile-and-payment-mix)](#financial-profile-and-payment-mix)

[Patient Flow to Out-of-System Healthcare [2](#patient-flow-to-out-of-system-healthcare)](#patient-flow-to-out-of-system-healthcare)

[Organizational Readiness for AI [2](#organizational-readiness-for-ai)](#organizational-readiness-for-ai)

[SOW Summary [3](#sow-summary)](#sow-summary)

[Phase 1 [4](#_Toc212473614)](#_Toc212473614)

[Overview [4](#overview)](#overview)

[FHIR Data Resources [4](#fhir-data-resources)](#fhir-data-resources)

[Needed Profiles [4](#needed-profiles)](#needed-profiles)

[Minimally Viable Data Set [5](#minimally-viable-data-set)](#minimally-viable-data-set)

[Minimally Viable FHIR eCQM Measures [5](#minimally-viable-fhir-ecqm-measures)](#minimally-viable-fhir-ecqm-measures)

[Attribution Hierarchies [5](#attribution-hierarchies)](#attribution-hierarchies)

[Document Resources [15](#document-resources)](#document-resources)

[Patient Data Dictionaries [15](#patient-data-dictionaries)](#patient-data-dictionaries)

[Health System Description [15](#health-system-description-1)](#health-system-description-1)

[IT Systems [15](#it-systems)](#it-systems)

[Metric Calculations [15](#metric-calculations)](#metric-calculations)

[Attribution [15](#attribution)](#attribution)

[Aggregate Calculations [16](#aggregate-calculations)](#aggregate-calculations)

[Collaboration Documentation [16](#collaboration-documentation)](#collaboration-documentation)

# Goal

This document describes critical aspects of the Andor Health System that are needed by Data Voyager to understand the organizational structure, patient population, IT systems, payer mix, and organizational readiness.

# Health System Description

## Organizational Structure and Staffing

The health system includes three hospitals (tertiary-350 beds, community-150 beds, critical access-25 beds) and a multi-specialty 400-provider group practice. Some providers are employed while others are affiliated independent practices in the clinically integrated network (CIN). There is a centralized Population Health Department with care coordinators and outreach specialists, a centralized business office for revenue cycle and payer contract management, and separate quality improvement and analytics teams.

## Patient Population Demographics

The system cares for 750,000 residents across multiple counties, including suburban, small urban, and rural populations. Payer mix is 40% Medicare (FFS and MA), 20% Medicaid (state and HMOs), 35% commercial (large employers, ACA plans), and 5% self-pay/uninsured. It is an aging populatin with a high prevalence of chronic conditions, diverse socioeconomic profiles (including low-income rural), and moderate racial/ethnic diversity with notable immigrant communities.

## IT Systems and Data Infrastructure

The system has implemented Epic for hospitals and ambulatory clinics with a single integrated instance. Population staff use Epic Healthy Planet for maintenance of registries and care management. There is an enterprise data warehouse aggregating Epic data, claims, and HIE feeds. The system has HL7 APIs for exchanging data with the state HIE. They use PowerBI for dashboards and SQL-based analytics for deeper queries.

## Financial Profile and Payment Mix

The system has patient service revenue from inpatient/outpatient care, clinic visits, and ancillary services. Revenue from shared savings and quality incentives are possible from MSSP, Medicaid managed care, and commercial ACO contracts. They previously had revenue from grants for community health initiatives, although many of these programs have been defunded recently. They participate in MSSP ACO Track 1+ (downside risk), bundled payments for joint replacement and cardiac care; Medicaid managed care with performance incentives for preventive screenings and chronic disease management;and commercial shared savings/risk contracts with major payers with some episode-based payment arrangements. There are three high-priority commercial payer contracts with significant performance incentives for preventive screenings and chronic disease management.

## Patient Flow to Out-of-System Healthcare

Some patients are seen at a separate community hospital that is geographically situated between Andor tertiary and community hospitals; this separate community hospital is not affiliated with the Andor Health System. It uses the Cerner EHR. This hospital participates in the state HIE.

There is also a significant sunbird and snowbird population that travels to Florida.

## Organizational Readiness for AI

They have an established quality reporting team producing dashboards, risk stratification models in use for high-risk patient targeting and care coordination, and standard workflows for pre-visit planning and care gap closure. They have pilots in clinical documentation assistance and patient messaging summarization.

# SOW Summary

The first use case for the Andor Health System is **closing comprehensive care gaps with a focus on high-risk populations**. Following are complete leadership and operations examples that describe the high-level functionality of the Data Voyager interface.

**Leadership Example** - An agent monitors comprehensive care delivery across 28,000 high-risk patients, surfacing population-wide gaps and their financial impact. Leadership dashboards identify that closing comprehensive gaps for \~420 high-complexity patients (missing AWVs + chronic condition documentation + overdue care gaps) would increase RAF revenue by \$3.2M annually and prevent an estimated \$1.8M in downstream hospitalizations. The system recommends expanding care management by 60%, targeting RAF-eligible populations, implementing automated claims-to-EHR reconciliation, and deploying mobile screening units.

**Operations Example** - An agent generates comprehensive care gap worklists for care coordinators that identify high-risk patients. Each patient entry displays integrated gap analysis, recommended care bundles, and auto-generated outreach materials. For a complex CHF patient, the system identifies \$5,400 in recoverable RAF value through condition documentation, creates personalized appointment scheduling accounting for transportation barriers, and pre-populates clinical templates with HCC-specific assessment prompts. Alerts flag time-sensitive opportunities, while escalation packets compile prior outreach attempts, social barriers, and specialist recommendations. The system tracks completion and generates follow-up workflows.

#### The first use case will be implemented in several phases

- **Phase 1** - Calculate metrics as care gaps and generate prioritized reports

- **Phase 2** - Calculate HCC gaps (diagnosis previously documented but not documented in payer year end) and AWV and generate prioritized reports with financial impact on RAF revenue

- **Integrate Phase 1 and Phase 2** -- summarize gaps and financial impact and generate prioritized reports

- **Phase 3** - Calculate risk scores and identify high-complexity patients for targeted efforts

  - HCC risk

  - SDOH

  - ED and hospitalizations

- Phase 4 -- Leadership recommendations and auto-generated outreach materials

  - Patient contact preferences

- Phase 5 -- Time trending and forecasting of completed gaps by years end based on prior trends

- Phase 6 -- Automated monitoring

  - Schedule for frequency of execution

- []{#_Toc212473614 .anchor}Phase 7 -- complete financial impact - calculate dollars at risk for leaving on the table based on payer thresholds????

# Phase 1

## Overview

This phase focuses on the following examples, which are subsets of the above examples.

- **Leadership Example** - An agent summarizes quality care gaps across 100,000 patients, surfacing population-wide gaps in care quality and their financial impact. Leadership dashboards identify that closing these care gaps (for example, overdue screenings, diabetes metrics, readmission metrics) would prevent an estimated \$2.8M in downstream hospitalizations.

- **Operations Example** - An agent generates prioritized care gap worklists for care coordinators. Each patient entry displays integrated gap analysis for that patient. For a complex CHF patient, the system identifies 3 care gaps that contribute significantly to preventable hospitalizations.

**Phase 1** - Calculate metrics as care gaps (against the payer year end) and generate prioritized reports with financial impact on downstream hospitalizations; generate care gap worklists for care coordinators by patient with list of open gaps, count of open gaps, count of open gaps that contribute significantly to downstream hospitalizations, and basic worklist fields (assigned PCP, date of last visit with PCP, date of last visit, basic contact information).

- FHIR metrics and CQL execution (plus libraries and valuesets from the bundles)

- Attribution to PCP, clinic/department/service line, hospital, health system

- Documentation of downstream hospitalizations, level of impact, and calculation for aggregate financial impact.

## FHIR Data Resources

### Needed Profiles

Store clinical data conformant to US Core; run measures against QI-Core views or transformations; return/share results using DEQM/Gaps-in-Care profiles and operations; manage rosters with ATR.

The following profiles are required:

**Foundational clinical data:**

US Core (R4): Patient, Condition, Observation, Procedure, Immunization, DiagnosticReport, MedicationRequest, MedicationStatement, Encounter, CarePlan, Practitioner, PractitionerRole, Organization, Location, Coverage, AllergyIntolerance, CareTeam, Device, ServiceRequest.

**Quality/measurement layer:**

QI-Core (R4): Logical profiles aligned to measure logic (CQL).

**Quality measures:**

Quality Measure Implementation Guide (QM IG)

**Reporting/exchange layer (care gaps):**

Da Vinci DEQM (R4) & Da Vinci Gaps in Care (R4) Implementation Guides.

**Attribution & roster management:**

Da Vinci Patient Attribution (ATR) (R4).

### Minimally Viable Data Set

**Patient, Practitioner, PractitionerRole, Organization, Location**

**Coverage** (and **Group (ATR)** for attribution)

**Encounter** (at least last 24 months)

**Condition** (problem list + key historical)

**Observation** (LOINC: A1c, LDL, BP; screenings; tobacco)

**Procedure** (colonoscopies, mammograms, cervical cancer screenings, eye exams)

**Immunization** (CVX)

**MedicationRequest/Statement** (statins; other measure meds)

**Measure, Library, MeasureReport** (+ DEQM/Gaps profiles)

**Provenance, OperationOutcome** (DQ & audit) -- OPTIONAL based on Synthea capabilities

### Minimally Viable FHIR eCQM Measures

Use the 10 measures from the CMS Connectathon testing

### Attribution Hierarchies

Here is a detailed narrative description of the fictional **Andor Health System** and its full attribution hierarchy, modeled to support value-based care, contract accountability, and patient paneling aligned with the HL7® Da Vinci Patient Attribution (ATR) Implementation Guide.

#### 1. Organizational Structure

**Andor Health System (AHS)** is a fully integrated regional health system serving approximately 750,000 residents across suburban, small urban, and rural regions. Its organizational structure is designed to support comprehensive clinical services and efficient value-based care coordination.

**1.1 Health System Entity**

- **Organization Name:** Andor Health System

- **FHIR Organization ID:** Organization/1

- **OID:** 2.16.840.1.113883.19.4.321.999.234

- **TIN:** 123456789

- **NPI:** *None (non-practicing org)*

- **Type:** prov (healthcare provider)

- **Role:** System-wide accountable entity for contracts and attribution

**1.2 Hospitals**

  --------------------------------------------------------------------------------------------
  **Hospital Name**          **Beds**   **Type**          **FHIR ID**   **CCN**   **NPI**
  -------------------------- ---------- ----------------- ------------- --------- ------------
  Andor Medical Center       350        Tertiary          Org/2         310001    3141592653

  Andor Community Hospital   150        Community         Org/3         310002    2718281828

Andor Rural Hospital       25         Critical Access   Org/4         310003    1414213569
  --------------------------------------------------------------------------------------------

Each is partOf Andor Health System.

**1.3 Outpatient Clinics (n = 12)**

Grouped by hospital region:

- **Primary Care Clinics (6):**

  - Family Medicine North (Location/101)

  - Family Medicine South (102)

  - Internal Medicine Clinic (103)

  - Pediatrics - Greenfield (104)

  - Rural Family Health Center (105)

  - Lakeview Pediatrics (106)

- **Specialty Clinics (6):**

  - Andor Heart Institute (107)

  - Orthopedic Center (108)

  - Oncology Center (109)

  - Women\'s Health & OBGYN (110)

  - Endocrinology & Diabetes Center (111)

  - Pulmonary Clinic (112)

Each clinic has a FHIR Location resource with an internal ID and a managing Organization (hospital).

**1.4 Departments & Service Lines**

Modeled using **Organization or HealthcareService** resources (type = dept), each partOf a clinic or hospital:

  --------------------------------------------------------------------------------------
  **Service Line**   **Departments Created (per hospital/clinic)**   **FHIR ID Range**
  ------------------ ----------------------------------------------- -------------------
  Primary Care       Family Med, Internal Med, Geriatrics            Org/20--22

  Pediatrics         General Pediatrics, Pediatric Asthma            Org/23--24

  Cardiology         General Cardiology, CHF Program                 Org/25--26

  Orthopedics        Joint Replacement, Sports Medicine              Org/27--28

  Oncology           Medical Oncology, Breast Cancer Navigation      Org/29--30

  Women\'s Health    OBGYN, Prenatal Care                            Org/31--32

  Endocrinology      Diabetes, Thyroid Care                          Org/33--34

Pulmonary          Asthma, COPD Programs                           Org/35--36
  --------------------------------------------------------------------------------------

These departments are referenced in attribution for contract programs involving specialty care or bundled payments.

#### 2. Provider Network & Attribution Roles

**2.1 Provider Summary**

- **Total Providers:** 400

  - **Employed by Andor Health System:** 250

  - **Affiliated via Clinically Integrated Network (CIN):** 150

- All providers have:

  - **NPI (10-digit)** and **internal ID** (e.g., AHSP-0001)

  - **Practitioner** resource and at least one **PractitionerRole**

  - Specialties coded using NUCC taxonomy (e.g., 207Q00000X for Family Medicine)

**2.2 Provider Attribution: Extension Patterns and Counts**

Each attributed patient is linked via Group.member.extension.attributedProvider, using:

  --------------------------------------------------------------------------------------------------------------
  **Provider Reference Type**   **Use Case**                                             **Count of Patients**
  ----------------------------- -------------------------------------------------------- -----------------------
  Practitioner                  Individual PCP (Family/Internal Medicine, Pediatrics)    \~70,000

  PractitionerRole              Specialist tied to clinic or department                  \~15,000

Organization                  Attributed to hospital/service line (e.g., for bundle)   \~15,000
  --------------------------------------------------------------------------------------------------------------

Examples:

- For Medicare ACO and commercial ACOs: attributedProvider → Practitioner

- For bundled payments: → Organization (e.g., Orthopedic Dept)

- For Medicaid pediatric program: → PractitionerRole (e.g., Pediatrician at rural health clinic)

Each provider's TIN and role are included in the Group identifier list.

#### 3. Payer & Coverage Structure

**3.1 Participating Payers**

Andor Health System maintains contracts with **8 major payers**, representing Medicare, Medicaid, and commercial lines of business:

  ---------------------------------------------------------------------------------
  **Payer Name**               **Payer Type**       **Identifier (NAIC or Code)**
  ---------------------------- -------------------- -------------------------------
  CMS Medicare FFS             Government           ---

  Sunrise Medicare Advantage   Medicare Advantage   70001

  Evergreen Medicare Adv.      Medicare Advantage   70002

  HealthOne Medicaid HMO       Medicaid             77001

  FamilyCare Medicaid HMO      Medicaid             77002

  HorizonHealth                Commercial           12345

  ClearBlue                    Commercial           98765

AxisBenefits                 Commercial           22233
  ---------------------------------------------------------------------------------

Each payer is represented as a FHIR Organization with organization-type = pay.

**3.2 Coverage Attribution**

- Each patient is assigned a FHIR Coverage resource referencing their payer.

- Coverage includes:

  - Coverage.payor: Payer organization reference

  - Coverage.class.value: Plan name or product

  - Coverage.period: Coverage period (e.g., for 2025)

  - Coverage.beneficiary: Patient reference

  - Optional: contract reference or crosswalk to panel via coverageReference extension in Groups

#### 4. Contracts & Risk Programs

**4.1 Value-Based Contracts**

Andor has **15 active value-based contracts** across its payers:

  ----------------------------------------------------------------------------------------------------------------------------
  **Contract ID**   **Payer**                               **Type**                              **Attribution Type**
  ----------------- --------------------------------------- ------------------------------------- ----------------------------
  C001              Medicare FFS                            ACO (MSSP)                            Organization

  C002--C005        MA plans                                Risk-sharing, quality bonus           PCP

  C006--C009        Medicaid HMOs                           ACO-like, quality incentive           PCP or pediatrician

  C010--C012        Commercial (Horizon, ClearBlue, Axis)   Shared savings, bundles, capitation   PCP, specialist, or clinic

C013--C015        Commercial quality                      Pay-for-performance                   PCP or dept
  ----------------------------------------------------------------------------------------------------------------------------

Each contract is modeled as a FHIR Contract resource:

- With an identifier (e.g., C001)

- Contract.period = 2025

- Contract.type = ACO, bundled, etc.

**4.2 Payer Mix and Contracts**

  -------------------------------------------------------------------------------------
  **Payer Name**        **Type**     **Contract Count**   **Sample Contract IDs**
  --------------------- ------------ -------------------- -----------------------------
  CMS Medicare FFS      Public       1                    C001 (ACO)

  Sunrise MA            MA           2                    C002 (Risk), C003 (Quality)

  Evergreen MA          MA           2                    C004, C005

  HealthOne Medicaid    Medicaid     2                    C006, C007

  FamilyCare Medicaid   Medicaid     2                    C008, C009

  HorizonHealth         Commercial   3                    C010--C012

  ClearBlue             Commercial   2                    C013, C014

AxisBenefits          Commercial   1                    C015
  -------------------------------------------------------------------------------------

Total: **15 contracts**, each with a **FHIR Contract** and associated **FHIR Group**.

#### 5. Patient Attribution Groups

**5.1 Group Resource Structure**

Each contract has a corresponding **FHIR Group** resource listing attributed patients.

Group resources include:

- Group.type = person

- Group.actual = true

- Group.identifier: NPI + TIN + contract ID

- Group.extension:

  - contractValidityPeriod: 2025

  - attributionListStatus: final

- Group.member\[\]: Each with:

  - entity: Patient/\<ID\>

  - period: Attribution period

  - extension.coverageReference: Coverage/\<ID\>

  - extension.attributedProvider: Practitioner, PractitionerRole, or Organization

**5.2 Attribution Assignment Logic**

Attribution is determined using:

- Payer (from Coverage)

- Provider specialty (primary care vs. specialist)

- Location (clinic, hospital, rural health)

- Insurance product (e.g., Medicaid HMO, commercial bundle)

Example mappings:

- **Medicare FFS (ACO):** Patients 65+, attributed to system or primary care provider

- **Sunrise MA Risk:** Attributed to individual PCPs

- **HealthOne Medicaid:** Pediatric and adult patients attributed to community providers

- **ClearBlue Bundled:** Patients who underwent joint replacement in 2025, attributed to orthopedic department

**Core Inputs for Attribution:**

- Coverage.payor.display → Payer

- Coverage.period.start → Contract year (2025)

- Patient **age**, **encounter history**, **clinic visits**

- Provider **specialty**, **role**, **organization**

**Contract-by-Contract Attribution Logic**

  -------------------------------------------------------------------------------------------------------------------------------------------
  **Contract ID**   **Type**               **Attribution Method**
  ----------------- ---------------------- --------------------------------------------------------------------------------------------------
  C001              Medicare ACO           Patients ≥65 with ≥1 visit to Family/Internal Med PCP in prior year → attributed to Practitioner

  C002/3            Sunrise MA             MA-covered patients with visits to PCP → Practitioner

  C004/5            Evergreen MA           Similar to C002; pediatrics eligible for Quality contract

  C006/7            HealthOne Medicaid     Pediatric patients seen in rural clinics → PractitionerRole for peds providers

  C008/9            FamilyCare Medicaid    Adult Medicaid enrollees seen in community clinics → Practitioner or PractitionerRole

  C010              HorizonHealth ACO      Commercial patients with \>1 PCP visit in 2024 → Practitioner

  C011              Horizon Quality        Attribution same as C010 + stratified by gaps

  C012              Horizon Bundled        Patients with hip/knee replacement episodes → attributed to Organization (Ortho Dept)

  C013/14           ClearBlue Contracts    Cardiology and Diabetes bundles → attributed to PractitionerRole (e.g., cardiologists)

C015              AxisBenefits Quality   Capitated plan, PCP assigned from Coverage.subscriber logic or last PCP seen
  -------------------------------------------------------------------------------------------------------------------------------------------

**Specialty alone is not used** for attribution; rather, **encounter type + provider role** is evaluated to infer attribution.

#### 6. Panels and Program Breakdown

  ---------------------------------------------------------------------------------------
  **Panel Type**      **Count**   **Description**
  ------------------- ----------- -------------------------------------------------------
  ACO Panels          5           Medicare Shared Savings, MA ACOs, Commercial ACOs

  Quality Incentive   5           Medicaid & Commercial P4P programs

  Bundled Payment     3           Joint replacement, CHF, diabetes (ClearBlue, Horizon)

  Capitated Panels    1           AxisBenefits - primary care total cost management

Pediatric Panels    1           Medicaid HMO - rural and underserved peds attribution
  ---------------------------------------------------------------------------------------

Total: **15 distinct FHIR Group resources**, each corresponding to a contract.

Each Group contains:

- Between **2,000 to 20,000** patients

- Group extensions:

  - contractValidityPeriod: 2025-01-01 to 2025-12-31

  - attributionListStatus: final

- Each member has:

  - Patient reference

  - Coverage reference

  - attributedProvider: Practitioner, PractitionerRole, or Organization

#### 7. Attribution Hierarchy Crosswalk

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Level**           **FHIR Resource Type**                               **Example**          **Description**
  ------------------- ---------------------------------------------------- -------------------- ----------------------------------------------------------------------
  Health System       Organization                                         Organization/1       Top-level entity managing contracts, risk, reporting

  Hospital            Organization                                         Organization/2       Acute care facility with inpatient/outpatient services

  Clinic              Location                                             Location/105         Physical site of care, managed by hospital

  Department          Organization (dept)                                  Organization/20      Logical or physical department (e.g., Cardiology, Pediatrics)

  Service Line        Organization (group) or [HealthcareService]{.mark}   Organization/50      Roll-up entity across departments (e.g., Orthopedics system-wide)

  Provider            Practitioner                                         Practitioner/1001    Licensed individual with NPI and specialty

  PCP Role            PractitionerRole                                     PractitionerRole/3   Ties provider to org + specialty + location

  CIN Affiliation     [OrganizationAffiliation]{.mark}                     N/A                  Connects independent providers to CIN org (optional)

  Payer               Organization                                         Organization/7       Insurance company / plan sponsor

  Contract            [Contract]{.mark}                                    Contract/C001        Agreement between AHS and payer with defined risk and quality terms

  Coverage            Coverage                                             Coverage/12345       Patient-level insurance enrollment

  Attribution Group   [Group]{.mark}                                       Group/1              List of attributed members under a contract

Member Entry        [Group.member]{.mark}                                Patient/xyz          Individual patient attribution including PCP and Coverage references
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------

[Yellow highlight]{.mark} are not part of the core FHIR resources exported by Synthea

#### 8. Linking Providers and Patients

The correct linkage model is:

- Patient ← Coverage → Payer

- Patient ← **assigned via Group.member** → attributedProvider

- attributedProvider is one of:

  - Practitioner: most common (PCP)

  - PractitionerRole: when provider role (e.g., peds in a location) matters

  - Organization: for bundled or org-attributed programs

- PractitionerRole links provider to:

  - Clinic (Location)

  - Department (Organization, type dept)

  - Specialty (e.g., Family Medicine)

Attribution is not inferred solely from Encounter.location. Instead, **encounter + role + specialty + payer** together determine which panel a patient is placed in.

#### 9. System Summary

- **100,000 patients** synthesized

- **400 providers** across 3 hospitals and 10 clinics

- **15 contracts**, each with its own **Group** attribution list

- Providers and patients linked via:

  - Coverage → payer

  - PCP → practitioner

  - Location → clinic/hospital

- Panels support:

  - **ACO** shared savings models

  - **Bundled payment** programs

  - **Capitation** and **P4P**

- **FHIR resources**: Organization, Practitioner, PractitionerRole, Location, Contract, Coverage, Group, Patient

#### 9. CSV Exports

1. **Organizational Hierarchy** -- Health system and hospital metadata (IDs, CCNs, TINs, NPIs)

2. **Payers** -- 8 payer organizations, NAIC codes, and ownership

3. **Clinics and Locations** -- All 12 clinic sites, types, and associated hospitals

4. **Contracts and Panels** -- All 15 contracts with types and attribution counts

5. **Providers** -- Full list of employed and CIN practitioners, specialties, NPIs

![](/home/claude/media/media/image1.emf)![](/home/claude/media/media/image2.emf)![](/home/claude/media/media/image3.emf)![](/home/claude/media/media/image4.emf)![](/home/claude/media/media/image5.emf)

## Document Resources

### Patient Data Dictionaries

- **Provider Clinical Data**: EHR data from Epic in FHIR format:

  - **FHIR Data Dictionary (R4)**: <https://hl7.org/fhir/R4/> (Recommended version 4.0.1)

- **FHIR Implementation Guides for Providers (Phase 1 Recommended Versions)**

  ----------------------------------------------------------------------------------------------------------------------
  **IG Name**                             **Recommended Version**   **Official Web Link**
  --------------------------------------- ------------------------- ----------------------------------------------------
  US Core Implementation Guide            6.1.0\*                   <http://hl7.org/fhir/us/core/STU6.1/>

  QI-Core                                 4.1.1                     <http://hl7.org/fhir/us/qicore/STU4.1.1/>

  Da Vinci DEQM & Gaps in Care IGs        3.0.0                     <https://build.fhir.org/ig/HL7/davinci-deqm/STU3/>

  Da Vinci Patient Attribution (ATR) IG   1.0.0                     <https://build.fhir.org/ig/HL7/davinci-atr/>

Bulk FHIR (Flat FHIR) API               1.0.1                     <https://hl7.org/fhir/uv/bulkdata/STU1.0.1/>
  ----------------------------------------------------------------------------------------------------------------------

> \*<https://www.linkedin.com/pulse/understanding-evolution-us-core-version-610-versus-chaudhary-pmp-wudke>

- **SQL-on-FHIR View:** JSDoc for the view of the FHIR R4 data

### Health System Description

- **Health System Description**: Knowledge of the health system including organizational structure and staffing, patient population demographics, IT systems and data infrastructure, financial profile and payment mix, patient flow to out-of-system healthcare, organizational readiness for AI.

### IT Systems

- **IT User Role and Permissions Data**: Assumption is that this will be Microsoft EntraID and Active Directory. Information about user roles and what they are allowed to see/do in each system. The agent should respect these permission levels (e.g., an analyst might retrieve aggregate data but not individual PHI, whereas a clinician can get patient specifics). Documentation of permission schemas and possibly integration with Active Directory (the mention of Azure AD in the Productive Edge case suggests using centralized identity).

### Metric Calculations

- **FHIR Standard Quality Metrics (FQM Engine)**: The initial list of FHIR CQL metrics includes the bundles from the 2025 CMS Connectathon. Ultimately, we should mirror executing these metrics nightly for care gaps.

> IG: <https://build.fhir.org/ig/cqframework/ecqm-content-cms-2025/index.html>
>
> GitHub: <https://github.com/cqframework/ecqm-content-cms-2025/?tab=readme-ov-file>

- CMS 2 - Preventive Care and Screening: Screening for Depression and Follow-up Plan Workflow

- CMS122 - Diabetes Hemoglobin A1c Poor Control

- CMS124 - Cervical Cancer Screening

- CMS125 - Breast Cancer Screening

- CMS130 - Colorectal Cancer Screening

- CMS165 - Controlling High Blood Pressure

- CMS529 - Hybrid Hospital-Wide Readmission

- CMS506 - Safe Use of Opioids - Concurrent Prescribing

- CMS816 - Hospital Harm: Severe Hypoglycemia and NHSN Hospital Safety Hypoglycemic Measure

- CMS1017 - Hospital Harm - Falls with Injury

- CMS1218 - Hospital Harm - Postoperative Respiratory Failure

### Attribution

- **Attributing Patient to PCP Documentation**: Documentation of how patients are attributed to PCPs. This should include via current PCP in Epic or through most frequent or most recent attribution algorithms.

- **Attributing Patient to Contract/Payer Documentation**: Documentation of how patients are attributed to payer contracts/payers. This should include via insurance plan codes in Epic or through payer lists.

- **Attributing Providers to Health System Organizations Documentation**: Documentation of attribution of providers to clinics/departments/service lines and then to hospital/health system or directly to health system.

### Aggregate Calculations

- **Avoidable Hospitalizations Documentation**: Documentation of how the financial impact of avoidable hospitalizations are calculated for leadership reports.

### Collaboration Documentation

- **Team Membership Rosters**: For each patient or program, the agent needs to know which roles/individuals are part of the care team. This information might come from an EHR care team module or an internal assignment list (e.g., primary care doctor, assigned case manager, consulting pharmacist, etc.). Up-to-date rosters allow the agent to include the right people in communications.

- **Team Roles and Responsibilities Guidelines**: Documentation of what each team member's typical responsibilities are, especially in a collaborative model. For instance, a protocol might say the pharmacist is responsible for med reconciliation post-discharge, the social worker handles SDOH needs, etc. The agent uses this knowledge to direct alerts appropriately. It's effectively the definition of professional roles in the context of team care.

# Phase 2

## Overview

This phase focuses on the following examples, which are subsets of the above examples.

- **Leadership Example** - An agent summarizes chronic condition documentation across 100,000 patients, surfacing population-wide gaps in undocumented HCC diagnoses and their financial impact. Leadership dashboards identify that documenting these diagnoses (for example, complex diabetes) would increase RAF revenue by \$4.2M annually.

- **Operations Example** - An agent generates HCC and AWV gap worklists for Clinical Documentation Improvement (CDI) coordinators. Each patient entry displays integrated gap analysis for that patient. For a complex CHF patient, the system identifies a missing AWV and \$5,400 in recoverable RAF value through condition documentation.

**Phase 2** - Calculate metrics as HCC gaps (against the payer year end) and AWV and generate prioritized reports with financial impact on RAF revenue; generate HCC gap worklists for CDI coordinators by patient with with list of open gaps including AWV, count of open gaps, patient-level priority score based on gap impact on RAF revenue and basic worklist fields.

- HCC metrics, valuesets and RAF scores to construct HCC cohort (numerator is yes or no)

- AWV metric and valueset -- anyone in Medicare ACO -- had a AWV in the payer year end

- Documentation of RAF revenue and calculations for patient-level prioritization

# Integrate Phase 2 with Phase 1

## Overview

This phase focuses on the following examples, which are subsets of the above examples.

- **Leadership Example** - An agent summarizes comprehensive care delivery across 100,000 patients, surfacing population-wide gaps in care quality and undocumented HCC diagnoses and their financial impact. Leadership dashboards identify that closing these gaps would prevent an estimated \$2.8M in downstream hospitalizations and increase RAF revenue by \$4.2M annually.

- **Operations Example** - An agent generates a single integrated prioritized gap worklist (care gaps and HCCs and AWV) for coordinators. Each patient entry displays integrated gap analysis for that patient. For a complex CHF patient, the system identifies 3 care gaps that contribute significantly to preventable hospitalizations and \$5,400 in recoverable RAF value through condition documentation.

**Phase 1+2** - Generate prioritized leadership reports with combined financial impact (downstream hospitalizations and RAF revenue); generate a combined gap worklist for coordinators by patient with list of open gaps including AWV, count of open gaps, count of open gaps with high RAF or preventable hospitalization impact, and basic worklist fields.

- Documentation of how to combine downstream hospitalizations and RAF revenue and calculations for prioritization

# Phase 3 builds on Phases 1 & 2

## Overview

This phase focuses on the following examples, which are subsets of the above examples.

- **Leadership Example** - An agent summarizes comprehensive care delivery across 28,000 high-risk patients, surfacing population-wide gaps in care quality and undocumented HCC diagnoses and their financial impact. Leadership dashboards identify that closing comprehensive gaps for \~420 high-complexity patients (missing AWVs + chronic condition documentation + overdue care gaps) would increase RAF revenue by \$3.2M annually and prevent an estimated \$1.8M in downstream hospitalizations.

- **Operations Example** - An agent generates a single integrated prioritized gap worklist (care gaps and HCCs) for coordinators that identifies high-risk patients. Each patient entry displays integrated gap analysis for that patient. For a complex CHF patient, the system identifies 3 care gaps that contribute significantly to preventable hospitalizations and \$5,400 in recoverable RAF value through condition documentation.

**Phase 3** - Calculate HCC scores and identify high-complexity patients for targeted efforts; generate a combined gap worklist for coordinators by patient that adds risk score and thresholds.

- Documentation of HCC score calculations

- SDOH information

- ED visits and hospitalizations

- Documentation of risk score calculations and thresholds

# Phase 4

**Leadership Example** - An agent monitors comprehensive care delivery across 28,000 high-risk patients, surfacing population-wide gaps and their financial impact. Leadership dashboards identify that closing comprehensive gaps for \~420 high-complexity patients (missing AWVs + chronic condition documentation + overdue screenings) would increase RAF revenue by \$3.2M annually and prevent an estimated \$1.8M in downstream hospitalizations. The system recommends expanding care management by 60%, targeting RAF-eligible populations, implementing automated claims-to-EHR reconciliation, and deploying mobile screening units.

**Operations Example** - An agent generates comprehensive care gap worklists for care coordinators that identify high-risk patients. Each patient entry displays integrated gap analysis, recommended care bundles, and auto-generated outreach materials. For a complex CHF patient, the system identifies \$5,400 in recoverable RAF value through condition documentation, creates personalized appointment scheduling accounting for transportation barriers, and pre-populates clinical templates with HCC-specific assessment prompts. Alerts flag time-sensitive opportunities, while escalation packets compile prior outreach attempts, social barriers, and specialist recommendations. The system tracks completion and generates follow-up workflows.

This phase focuses on the following examples, which are subsets of the above examples.

- **Leadership Example** - An agent summarizes comprehensive care delivery across 28,000 high-risk patients, surfacing population-wide gaps in care quality and undocumented HCC diagnoses and their financial impact. Leadership dashboards identify that closing comprehensive gaps for \~420 high-complexity patients (missing AWVs + chronic condition documentation + overdue care gaps) would increase RAF revenue by \$3.2M annually and prevent an estimated \$1.8M in downstream hospitalizations.

- **Operations Example** - An agent generates a single integrated prioritized gap worklist (care gaps and HCCs) for coordinators that identifies high-risk patients. Each patient entry displays integrated gap analysis for that patient. For a complex CHF patient, the system identifies 3 care gaps that contribute significantly to preventable hospitalizations and \$5,400 in recoverable RAF value through condition documentation.

**Phase 4** - Leadership recommendations and auto-generated outreach materials

- Patient contact preferences
