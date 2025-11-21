#!/usr/bin/env python3
"""
temporal_analysis_implementation.py
Implementation of Dr. Smith's Temporal Analysis Methodology
Symphony Corps - Data Voyager Team
Last Updated: November 21, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import json
import zipfile
import csv
import io
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# Data Structures
# ============================================================================

class EncounterClass(Enum):
    """CMS encounter classifications"""
    AMB = "ambulatory"          # Outpatient
    EMER = "emergency"           # Emergency
    IMP = "inpatient"            # Inpatient
    WELLNESS = "wellness"        # Annual Wellness Visit
    URGENTCARE = "urgentcare"    # Urgent Care
    VIRTUAL = "virtual"          # Telehealth

class RiskTier(Enum):
    """Patient risk stratification tiers"""
    CRITICAL = 4
    HIGH = 3
    MODERATE = 2
    LOW = 1

class GapSeverity(Enum):
    """Care gap severity levels"""
    CRITICAL = "2+ years without care"
    HIGH = "18+ months without care"
    MODERATE = "12+ months without care"
    LOW = "Under 12 months"

@dataclass
class TemporalEvent:
    """Represents a single temporal event in patient timeline"""
    patient_id: str
    date: datetime
    resource_type: str
    encounter_class: Optional[str]
    description: str
    code: Optional[str]
    value: Optional[str]
    provider_id: Optional[str]
    
    def __lt__(self, other):
        return self.date < other.date

@dataclass
class CareGap:
    """Represents a gap in care continuity"""
    patient_id: str
    start_date: datetime
    end_date: datetime
    duration_days: int
    severity: GapSeverity
    gap_type: str
    financial_impact: float

@dataclass
class AttributionResult:
    """PCP attribution result with confidence metrics"""
    patient_id: str
    attributed_pcp_id: str
    attribution_method: str
    confidence_score: float
    encounter_count: int
    last_visit_date: datetime

# ============================================================================
# Temporal Data Extraction
# ============================================================================

class TemporalDataExtractor:
    """Extract and process temporal data from Synthea outputs"""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.resource_files = [
            'encounters.csv',
            'conditions.csv',
            'procedures.csv',
            'observations.csv',
            'medications.csv',
            'payer_transitions.csv'
        ]
    
    def extract_patient_timeline(self, patient_id: str) -> pd.DataFrame:
        """
        Extract comprehensive temporal sequence for a patient
        Following Dr. Smith's first-principles approach
        """
        timeline_events = []
        
        # Process each resource type
        for resource_file in self.resource_files:
            events = self._extract_resource_events(patient_id, resource_file)
            timeline_events.extend(events)
        
        # Sort chronologically
        timeline_events.sort()
        
        # Convert to DataFrame
        df = pd.DataFrame([vars(e) for e in timeline_events])
        df['date'] = pd.to_datetime(df['date'])
        
        return df
    
    def _extract_resource_events(self, patient_id: str, resource_file: str) -> List[TemporalEvent]:
        """Extract events from a specific resource CSV"""
        events = []
        file_path = f"{self.data_path}/{resource_file}"
        
        try:
            df = pd.read_csv(file_path)
            
            # Filter for patient
            patient_data = df[df['PATIENT'] == patient_id]
            
            for _, row in patient_data.iterrows():
                # Extract date
                event_date = self._parse_date(row)
                if event_date is None:
                    continue
                
                # Create event based on resource type
                event = self._create_temporal_event(
                    patient_id, 
                    event_date,
                    resource_file.replace('.csv', ''),
                    row
                )
                events.append(event)
                
        except Exception as e:
            print(f"Error processing {resource_file}: {e}")
        
        return events
    
    def _parse_date(self, row: pd.Series) -> Optional[datetime]:
        """Parse date from various possible columns"""
        for date_col in ['START', 'DATE', 'STOP', 'END']:
            if date_col in row and pd.notna(row[date_col]):
                try:
                    return pd.to_datetime(row[date_col])
                except:
                    continue
        return None
    
    def _create_temporal_event(self, patient_id: str, date: datetime, 
                               resource_type: str, row: pd.Series) -> TemporalEvent:
        """Create TemporalEvent from row data"""
        return TemporalEvent(
            patient_id=patient_id,
            date=date,
            resource_type=resource_type,
            encounter_class=row.get('ENCOUNTERCLASS'),
            description=row.get('DESCRIPTION', ''),
            code=row.get('CODE'),
            value=row.get('VALUE'),
            provider_id=row.get('PROVIDER')
        )

# ============================================================================
# Care Gap Detection
# ============================================================================

class CareGapAnalyzer:
    """Analyze temporal patterns to identify care gaps"""
    
    def __init__(self, timeline_df: pd.DataFrame):
        self.timeline = timeline_df
        self.gaps = []
    
    def identify_all_gaps(self) -> List[CareGap]:
        """Comprehensive gap detection following Dr. Smith's methodology"""
        self.gaps = []
        
        # Primary care continuity gaps
        self.gaps.extend(self._detect_primary_care_gaps())
        
        # Chronic condition monitoring gaps
        self.gaps.extend(self._detect_diabetes_monitoring_gaps())
        self.gaps.extend(self._detect_hypertension_monitoring_gaps())
        
        # Preventive care gaps
        self.gaps.extend(self._detect_wellness_visit_gaps())
        self.gaps.extend(self._detect_screening_gaps())
        
        # Transition of care gaps
        self.gaps.extend(self._detect_transition_gaps())
        
        return self.gaps
    
    def _detect_primary_care_gaps(self) -> List[CareGap]:
        """Detect gaps in primary care continuity"""
        gaps = []
        
        # Filter ambulatory encounters
        amb_encounters = self.timeline[
            self.timeline['encounter_class'].isin(['ambulatory', 'wellness'])
        ].sort_values('date')
        
        if len(amb_encounters) < 2:
            return gaps
        
        # Check for gaps between consecutive visits
        for i in range(1, len(amb_encounters)):
            prev_date = amb_encounters.iloc[i-1]['date']
            curr_date = amb_encounters.iloc[i]['date']
            days_between = (curr_date - prev_date).days
            
            if days_between > 365:
                severity = self._classify_gap_severity(days_between)
                gap = CareGap(
                    patient_id=self.timeline['patient_id'].iloc[0],
                    start_date=prev_date,
                    end_date=curr_date,
                    duration_days=days_between,
                    severity=severity,
                    gap_type="Primary Care Continuity",
                    financial_impact=self._calculate_gap_impact(days_between)
                )
                gaps.append(gap)
        
        return gaps
    
    def _detect_diabetes_monitoring_gaps(self) -> List[CareGap]:
        """Detect gaps in diabetes monitoring (HbA1c testing)"""
        gaps = []
        
        # Check if patient has diabetes
        has_diabetes = self.timeline[
            self.timeline['description'].str.contains('diabetes', case=False, na=False)
        ].any().any()
        
        if not has_diabetes:
            return gaps
        
        # Find HbA1c tests
        hba1c_tests = self.timeline[
            self.timeline['description'].str.contains('A1c|HbA1c|Hemoglobin A1c', 
                                                     case=False, na=False)
        ].sort_values('date')
        
        # Group by year and check frequency
        if not hba1c_tests.empty:
            hba1c_tests['year'] = pd.to_datetime(hba1c_tests['date']).dt.year
            yearly_counts = hba1c_tests.groupby('year').size()
            
            for year, count in yearly_counts.items():
                if count < 2:  # Should have at least 2 per year
                    gap = CareGap(
                        patient_id=self.timeline['patient_id'].iloc[0],
                        start_date=datetime(year, 1, 1),
                        end_date=datetime(year, 12, 31),
                        duration_days=365,
                        severity=GapSeverity.MODERATE,
                        gap_type=f"Insufficient HbA1c Monitoring ({count}/2 required)",
                        financial_impact=1500.0  # Estimated cost of poor diabetes control
                    )
                    gaps.append(gap)
        
        return gaps
    
    def _detect_wellness_visit_gaps(self) -> List[CareGap]:
        """Detect missing Annual Wellness Visits"""
        gaps = []
        
        # Find AWV encounters
        awv_encounters = self.timeline[
            (self.timeline['description'].str.contains('wellness|annual', case=False, na=False)) |
            (self.timeline['encounter_class'] == 'wellness')
        ]
        
        if not awv_encounters.empty:
            awv_encounters['year'] = pd.to_datetime(awv_encounters['date']).dt.year
            years_with_awv = set(awv_encounters['year'].unique())
            
            # Check all years in timeline
            timeline_years = pd.to_datetime(self.timeline['date']).dt.year.unique()
            
            for year in timeline_years:
                if year not in years_with_awv:
                    gap = CareGap(
                        patient_id=self.timeline['patient_id'].iloc[0],
                        start_date=datetime(year, 1, 1),
                        end_date=datetime(year, 12, 31),
                        duration_days=365,
                        severity=GapSeverity.MODERATE,
                        gap_type="Missing Annual Wellness Visit",
                        financial_impact=500.0  # Lost preventive care opportunity
                    )
                    gaps.append(gap)
        
        return gaps
    
    def _detect_hypertension_monitoring_gaps(self) -> List[CareGap]:
        """Detect gaps in blood pressure monitoring for hypertensive patients"""
        gaps = []
        
        # Check if patient has hypertension
        has_htn = self.timeline[
            self.timeline['description'].str.contains('hypertension|HTN', case=False, na=False)
        ].any().any()
        
        if not has_htn:
            return gaps
        
        # Find BP measurements
        bp_obs = self.timeline[
            self.timeline['description'].str.contains('blood pressure|BP|systolic|diastolic', 
                                                     case=False, na=False)
        ].sort_values('date')
        
        # Check for quarterly monitoring
        if not bp_obs.empty:
            for i in range(1, len(bp_obs)):
                days_between = (bp_obs.iloc[i]['date'] - bp_obs.iloc[i-1]['date']).days
                if days_between > 120:  # More than 4 months
                    gap = CareGap(
                        patient_id=self.timeline['patient_id'].iloc[0],
                        start_date=bp_obs.iloc[i-1]['date'],
                        end_date=bp_obs.iloc[i]['date'],
                        duration_days=days_between,
                        severity=GapSeverity.MODERATE,
                        gap_type="Hypertension Monitoring Gap",
                        financial_impact=800.0
                    )
                    gaps.append(gap)
        
        return gaps
    
    def _detect_screening_gaps(self) -> List[CareGap]:
        """Detect gaps in preventive screenings"""
        gaps = []
        
        # Depression screening (PHQ-9)
        depression_screens = self.timeline[
            self.timeline['description'].str.contains('PHQ-9|depression screen', 
                                                     case=False, na=False)
        ]
        
        if depression_screens.empty:
            # Check if patient has been seen in past year
            recent_encounters = self.timeline[
                self.timeline['date'] > datetime.now() - timedelta(days=365)
            ]
            if not recent_encounters.empty:
                gap = CareGap(
                    patient_id=self.timeline['patient_id'].iloc[0],
                    start_date=datetime.now() - timedelta(days=365),
                    end_date=datetime.now(),
                    duration_days=365,
                    severity=GapSeverity.LOW,
                    gap_type="Missing Depression Screening",
                    financial_impact=200.0
                )
                gaps.append(gap)
        
        return gaps
    
    def _detect_transition_gaps(self) -> List[CareGap]:
        """Detect gaps in care transitions (post-discharge follow-up)"""
        gaps = []
        
        # Find hospitalizations
        hospitalizations = self.timeline[
            self.timeline['encounter_class'] == 'inpatient'
        ].sort_values('date')
        
        for _, hosp in hospitalizations.iterrows():
            discharge_date = hosp['date']
            
            # Look for follow-up within 30 days
            follow_ups = self.timeline[
                (self.timeline['date'] > discharge_date) &
                (self.timeline['date'] <= discharge_date + timedelta(days=30)) &
                (self.timeline['encounter_class'].isin(['ambulatory', 'wellness']))
            ]
            
            if follow_ups.empty:
                gap = CareGap(
                    patient_id=self.timeline['patient_id'].iloc[0],
                    start_date=discharge_date,
                    end_date=discharge_date + timedelta(days=30),
                    duration_days=30,
                    severity=GapSeverity.HIGH,
                    gap_type="Missing Post-Discharge Follow-up",
                    financial_impact=5000.0  # Potential readmission cost
                )
                gaps.append(gap)
            elif not follow_ups[follow_ups['date'] <= discharge_date + timedelta(days=7)].empty:
                # No follow-up within TCM window (7 days)
                gap = CareGap(
                    patient_id=self.timeline['patient_id'].iloc[0],
                    start_date=discharge_date,
                    end_date=discharge_date + timedelta(days=7),
                    duration_days=7,
                    severity=GapSeverity.MODERATE,
                    gap_type="Delayed Post-Discharge Follow-up",
                    financial_impact=2000.0
                )
                gaps.append(gap)
        
        return gaps
    
    def _classify_gap_severity(self, days: int) -> GapSeverity:
        """Classify gap severity based on duration"""
        if days >= 730:  # 2+ years
            return GapSeverity.CRITICAL
        elif days >= 540:  # 18+ months
            return GapSeverity.HIGH
        elif days >= 365:  # 12+ months
            return GapSeverity.MODERATE
        else:
            return GapSeverity.LOW
    
    def _calculate_gap_impact(self, days: int) -> float:
        """Calculate financial impact of care gap"""
        base_impact = 1000.0
        if days >= 730:
            return base_impact * 3.0
        elif days >= 540:
            return base_impact * 2.0
        elif days >= 365:
            return base_impact * 1.5
        else:
            return base_impact

# ============================================================================
# PCP Attribution
# ============================================================================

class PCPAttributor:
    """Attribute patients to PCPs using Dr. Smith's plurality logic"""
    
    def __init__(self, pcp_list: pd.DataFrame):
        self.pcp_list = pcp_list
        self.pcp_specialties = [
            'Family Medicine',
            'Internal Medicine',
            'Pediatrics',
            'Geriatrics',
            'Obstetrics & Gynecology'
        ]
    
    def attribute_patient_to_pcp(self, timeline: pd.DataFrame) -> AttributionResult:
        """
        Attribute patient to PCP using temporal plurality with recency weighting
        """
        # Filter qualifying encounters
        qualifying_encounters = timeline[
            timeline['encounter_class'].isin(['ambulatory', 'wellness', 'urgentcare'])
        ]
        
        if qualifying_encounters.empty:
            return None
        
        # Calculate provider scores
        provider_scores = self._calculate_provider_scores(qualifying_encounters)
        
        # Select PCP with highest score
        if not provider_scores:
            return None
        
        best_provider = max(provider_scores.items(), 
                          key=lambda x: (x[1]['continuity_score'], x[1]['count']))
        
        return AttributionResult(
            patient_id=timeline['patient_id'].iloc[0],
            attributed_pcp_id=best_provider[0],
            attribution_method='Plurality with Recency Weighting',
            confidence_score=self._calculate_confidence(best_provider[1], provider_scores),
            encounter_count=best_provider[1]['count'],
            last_visit_date=best_provider[1]['last_visit']
        )
    
    def _calculate_provider_scores(self, encounters: pd.DataFrame) -> Dict:
        """Calculate continuity scores for each provider"""
        provider_scores = {}
        current_date = datetime.now()
        
        for _, encounter in encounters.iterrows():
            provider_id = encounter.get('provider_id')
            if not provider_id:
                continue
            
            if provider_id not in provider_scores:
                provider_scores[provider_id] = {
                    'count': 0,
                    'continuity_score': 0.0,
                    'last_visit': None
                }
            
            # Increment count
            provider_scores[provider_id]['count'] += 1
            
            # Calculate recency weight (exponential decay)
            days_ago = (current_date - encounter['date']).days
            recency_weight = np.exp(-days_ago / 365)  # 1-year half-life
            
            # Add to continuity score
            provider_scores[provider_id]['continuity_score'] += recency_weight
            
            # Update last visit
            if (provider_scores[provider_id]['last_visit'] is None or 
                encounter['date'] > provider_scores[provider_id]['last_visit']):
                provider_scores[provider_id]['last_visit'] = encounter['date']
        
        return provider_scores
    
    def _calculate_confidence(self, selected_provider: Dict, all_scores: Dict) -> float:
        """Calculate confidence in attribution decision"""
        if len(all_scores) == 1:
            return 1.0
        
        total_score = sum(p['continuity_score'] for p in all_scores.values())
        if total_score == 0:
            return 0.0
        
        return selected_provider['continuity_score'] / total_score

# ============================================================================
# Quality Measure Calculator
# ============================================================================

class QualityMeasureCalculator:
    """Calculate eCQM measures with temporal logic"""
    
    def __init__(self, timeline: pd.DataFrame):
        self.timeline = timeline
    
    def calculate_cms122(self) -> Dict:
        """CMS122 - Diabetes: HbA1c Poor Control (>9%)"""
        # Check if patient has diabetes
        has_diabetes = self._has_condition('diabetes')
        if not has_diabetes:
            return {'eligible': False, 'numerator': None, 'measure': 'CMS122'}
        
        # Find most recent HbA1c
        hba1c_tests = self.timeline[
            self.timeline['description'].str.contains('A1c|HbA1c', case=False, na=False)
        ].sort_values('date', ascending=False)
        
        if hba1c_tests.empty:
            return {
                'eligible': True,
                'numerator': None,
                'measure': 'CMS122',
                'gap': 'No HbA1c test found'
            }
        
        most_recent = hba1c_tests.iloc[0]
        value = float(most_recent['value']) if pd.notna(most_recent['value']) else None
        
        return {
            'eligible': True,
            'numerator': value > 9.0 if value else None,
            'measure': 'CMS122',
            'last_value': value,
            'last_date': most_recent['date']
        }
    
    def calculate_cms2(self) -> Dict:
        """CMS2 - Preventive Care: Depression Screening"""
        # Check if patient already has depression diagnosis
        has_depression = self._has_condition('depression|major depressive')
        
        if has_depression:
            return {
                'eligible': False,
                'reason': 'Active depression diagnosis',
                'measure': 'CMS2'
            }
        
        # Look for PHQ-9 screening in past year
        one_year_ago = datetime.now() - timedelta(days=365)
        recent_screens = self.timeline[
            (self.timeline['description'].str.contains('PHQ-9|depression screen', 
                                                       case=False, na=False)) &
            (self.timeline['date'] > one_year_ago)
        ]
        
        return {
            'eligible': True,
            'numerator': not recent_screens.empty,
            'measure': 'CMS2',
            'last_screen': recent_screens.iloc[0]['date'] if not recent_screens.empty else None
        }
    
    def calculate_cms165(self) -> Dict:
        """CMS165 - Controlling High Blood Pressure"""
        # Check if patient has hypertension
        has_htn = self._has_condition('hypertension|HTN|high blood pressure')
        if not has_htn:
            return {'eligible': False, 'numerator': None, 'measure': 'CMS165'}
        
        # Find most recent BP reading
        bp_readings = self.timeline[
            self.timeline['description'].str.contains('blood pressure|BP|systolic', 
                                                     case=False, na=False)
        ].sort_values('date', ascending=False)
        
        if bp_readings.empty:
            return {
                'eligible': True,
                'numerator': None,
                'measure': 'CMS165',
                'gap': 'No BP reading found'
            }
        
        most_recent = bp_readings.iloc[0]
        
        # Parse BP value (format: "140/90")
        bp_controlled = self._parse_bp_control(most_recent['value'])
        
        return {
            'eligible': True,
            'numerator': bp_controlled,
            'measure': 'CMS165',
            'last_bp': most_recent['value'],
            'last_date': most_recent['date']
        }
    
    def _has_condition(self, condition_pattern: str) -> bool:
        """Check if patient has a specific condition"""
        return self.timeline[
            self.timeline['description'].str.contains(condition_pattern, 
                                                     case=False, na=False)
        ].any().any()
    
    def _parse_bp_control(self, bp_value: str) -> bool:
        """Parse BP value and check if controlled (<140/90)"""
        if not bp_value or pd.isna(bp_value):
            return None
        
        try:
            if '/' in str(bp_value):
                systolic, diastolic = str(bp_value).split('/')
                systolic = float(systolic)
                diastolic = float(diastolic)
                return systolic < 140 and diastolic < 90
        except:
            return None
        
        return None

# ============================================================================
# Temporal Pattern Analyzer
# ============================================================================

class TemporalPatternAnalyzer:
    """Advanced temporal pattern recognition and analysis"""
    
    def __init__(self, timeline: pd.DataFrame):
        self.timeline = timeline
    
    def analyze_disease_progression(self) -> List[Dict]:
        """Identify disease progression patterns"""
        progressions = []
        
        # Prediabetes to Diabetes
        prediabetes_onset = self._find_condition_onset('prediabetes')
        diabetes_onset = self._find_condition_onset('diabetes')
        
        if prediabetes_onset and diabetes_onset and diabetes_onset > prediabetes_onset:
            years_to_progress = (diabetes_onset - prediabetes_onset).days / 365
            progressions.append({
                'sequence': 'Prediabetes → Type 2 Diabetes',
                'start_date': prediabetes_onset,
                'end_date': diabetes_onset,
                'duration_years': round(years_to_progress, 1),
                'preventable': years_to_progress > 2,
                'intervention_window': 'Lifestyle modification could have prevented'
            })
        
        # Hypertension to Cardiovascular Event
        htn_onset = self._find_condition_onset('hypertension')
        cv_event = self._find_first_event(['myocardial infarction', 'stroke', 'heart failure'])
        
        if htn_onset and cv_event and cv_event > htn_onset:
            years_to_event = (cv_event - htn_onset).days / 365
            progressions.append({
                'sequence': 'Hypertension → Cardiovascular Event',
                'start_date': htn_onset,
                'end_date': cv_event,
                'duration_years': round(years_to_event, 1),
                'preventable': True,
                'intervention_window': 'BP control could have reduced risk'
            })
        
        return progressions
    
    def calculate_utilization_pattern(self) -> Dict:
        """Calculate healthcare utilization patterns"""
        # Count encounters by type
        encounter_counts = self.timeline.groupby('encounter_class').size().to_dict()
        
        # Calculate ED utilization rate
        ed_visits_12mo = len(self.timeline[
            (self.timeline['encounter_class'] == 'emergency') &
            (self.timeline['date'] > datetime.now() - timedelta(days=365))
        ])
        
        # Calculate admission rate
        admissions_12mo = len(self.timeline[
            (self.timeline['encounter_class'] == 'inpatient') &
            (self.timeline['date'] > datetime.now() - timedelta(days=365))
        ])
        
        # Identify high utilizer status
        is_high_utilizer = ed_visits_12mo >= 3 or admissions_12mo >= 2
        
        return {
            'total_encounters': len(self.timeline),
            'encounter_distribution': encounter_counts,
            'ed_visits_12mo': ed_visits_12mo,
            'admissions_12mo': admissions_12mo,
            'is_high_utilizer': is_high_utilizer,
            'utilization_score': ed_visits_12mo + (admissions_12mo * 3),
            'risk_tier': self._calculate_risk_tier(ed_visits_12mo, admissions_12mo)
        }
    
    def identify_care_patterns(self) -> Dict:
        """Identify patterns in care delivery"""
        patterns = {}
        
        # Regular vs irregular care pattern
        amb_encounters = self.timeline[
            self.timeline['encounter_class'] == 'ambulatory'
        ]['date'].tolist()
        
        if len(amb_encounters) > 2:
            intervals = [(amb_encounters[i+1] - amb_encounters[i]).days 
                        for i in range(len(amb_encounters)-1)]
            
            avg_interval = np.mean(intervals)
            std_interval = np.std(intervals)
            cv = std_interval / avg_interval if avg_interval > 0 else 0
            
            patterns['care_regularity'] = {
                'average_days_between_visits': round(avg_interval, 1),
                'standard_deviation': round(std_interval, 1),
                'coefficient_of_variation': round(cv, 2),
                'pattern': 'Regular' if cv < 0.5 else 'Irregular'
            }
        
        # Weekend vs weekday preference
        self.timeline['weekday'] = pd.to_datetime(self.timeline['date']).dt.dayofweek
        weekend_visits = len(self.timeline[self.timeline['weekday'].isin([5, 6])])
        weekday_visits = len(self.timeline[~self.timeline['weekday'].isin([5, 6])])
        
        patterns['visit_timing'] = {
            'weekend_visits': weekend_visits,
            'weekday_visits': weekday_visits,
            'weekend_percentage': round(weekend_visits / len(self.timeline) * 100, 1) if len(self.timeline) > 0 else 0
        }
        
        return patterns
    
    def _find_condition_onset(self, condition: str) -> Optional[datetime]:
        """Find first occurrence of a condition"""
        condition_events = self.timeline[
            self.timeline['description'].str.contains(condition, case=False, na=False)
        ]
        
        if not condition_events.empty:
            return condition_events['date'].min()
        return None
    
    def _find_first_event(self, event_patterns: List[str]) -> Optional[datetime]:
        """Find first occurrence of any event in list"""
        pattern = '|'.join(event_patterns)
        events = self.timeline[
            self.timeline['description'].str.contains(pattern, case=False, na=False)
        ]
        
        if not events.empty:
            return events['date'].min()
        return None
    
    def _calculate_risk_tier(self, ed_visits: int, admissions: int) -> str:
        """Calculate patient risk tier based on utilization"""
        if ed_visits >= 3 or admissions >= 2:
            return RiskTier.CRITICAL.name
        elif ed_visits >= 2 or admissions >= 1:
            return RiskTier.HIGH.name
        elif ed_visits >= 1:
            return RiskTier.MODERATE.name
        else:
            return RiskTier.LOW.name

# ============================================================================
# Report Generator
# ============================================================================

class TemporalAnalysisReport:
    """Generate comprehensive temporal analysis reports"""
    
    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        self.extractor = TemporalDataExtractor('./data')
        self.timeline = None
        self.gaps = []
        self.attribution = None
        self.measures = {}
        self.patterns = {}
    
    def generate_full_report(self) -> Dict:
        """Generate complete temporal analysis report"""
        print(f"Generating temporal analysis for patient {self.patient_id}")
        
        # Extract timeline
        print("  Extracting patient timeline...")
        self.timeline = self.extractor.extract_patient_timeline(self.patient_id)
        
        # Analyze gaps
        print("  Analyzing care gaps...")
        gap_analyzer = CareGapAnalyzer(self.timeline)
        self.gaps = gap_analyzer.identify_all_gaps()
        
        # Attribute PCP
        print("  Attributing primary care provider...")
        # Note: Would need actual PCP list in production
        # attributor = PCPAttributor(pcp_list_df)
        # self.attribution = attributor.attribute_patient_to_pcp(self.timeline)
        
        # Calculate quality measures
        print("  Calculating quality measures...")
        measure_calc = QualityMeasureCalculator(self.timeline)
        self.measures = {
            'CMS122': measure_calc.calculate_cms122(),
            'CMS2': measure_calc.calculate_cms2(),
            'CMS165': measure_calc.calculate_cms165()
        }
        
        # Analyze patterns
        print("  Analyzing temporal patterns...")
        pattern_analyzer = TemporalPatternAnalyzer(self.timeline)
        self.patterns = {
            'disease_progression': pattern_analyzer.analyze_disease_progression(),
            'utilization': pattern_analyzer.calculate_utilization_pattern(),
            'care_patterns': pattern_analyzer.identify_care_patterns()
        }
        
        # Compile report
        report = {
            'patient_id': self.patient_id,
            'analysis_date': datetime.now().isoformat(),
            'timeline_summary': {
                'total_events': len(self.timeline),
                'date_range': {
                    'start': self.timeline['date'].min().isoformat() if not self.timeline.empty else None,
                    'end': self.timeline['date'].max().isoformat() if not self.timeline.empty else None
                },
                'event_types': self.timeline['resource_type'].value_counts().to_dict()
            },
            'care_gaps': [
                {
                    'type': gap.gap_type,
                    'severity': gap.severity.name,
                    'duration_days': gap.duration_days,
                    'financial_impact': gap.financial_impact,
                    'start_date': gap.start_date.isoformat(),
                    'end_date': gap.end_date.isoformat()
                } for gap in self.gaps
            ],
            'quality_measures': self.measures,
            'temporal_patterns': self.patterns,
            'risk_assessment': {
                'total_gap_impact': sum(gap.financial_impact for gap in self.gaps),
                'critical_gaps': len([g for g in self.gaps if g.severity == GapSeverity.CRITICAL]),
                'high_utilizer': self.patterns.get('utilization', {}).get('is_high_utilizer', False),
                'risk_tier': self.patterns.get('utilization', {}).get('risk_tier', 'UNKNOWN')
            }
        }
        
        return report
    
    def save_report(self, output_path: str):
        """Save report to JSON file"""
        report = self.generate_full_report()
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Report saved to {output_path}")
        return report

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function for temporal analysis"""
    
    # Example patient ID (from Dr. Smith's documentation)
    patient_id = "624c651e-8c7c-48e5-8ff5-4df3f219d24c"
    
    # Generate report
    report_gen = TemporalAnalysisReport(patient_id)
    report = report_gen.generate_full_report()
    
    # Print summary
    print("\n" + "="*60)
    print("TEMPORAL ANALYSIS SUMMARY")
    print("="*60)
    print(f"Patient ID: {report['patient_id']}")
    print(f"Analysis Date: {report['analysis_date']}")
    print(f"Total Events: {report['timeline_summary']['total_events']}")
    print(f"Care Gaps Identified: {len(report['care_gaps'])}")
    print(f"Total Financial Impact: ${report['risk_assessment']['total_gap_impact']:,.2f}")
    print(f"Risk Tier: {report['risk_assessment']['risk_tier']}")
    
    # Print critical gaps
    critical_gaps = [g for g in report['care_gaps'] if 'CRITICAL' in g['severity']]
    if critical_gaps:
        print(f"\nCRITICAL GAPS ({len(critical_gaps)}):")
        for gap in critical_gaps:
            print(f"  - {gap['type']}: {gap['duration_days']} days")
    
    # Print quality measures
    print("\nQUALITY MEASURES:")
    for measure_name, result in report['quality_measures'].items():
        if result.get('eligible'):
            status = "PASS" if result.get('numerator') else "FAIL"
            print(f"  {measure_name}: {status}")
    
    # Save full report
    output_file = f"temporal_analysis_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_gen.save_report(output_file)

if __name__ == "__main__":
    main()
