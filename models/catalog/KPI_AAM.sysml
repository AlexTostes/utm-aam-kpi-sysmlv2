// KPI_AAM.sysml
// AAM domain (UAM as urban subset): 11 Performance Objectives and 17 KPI candidates (article 1, Table 4), anchored in the FAA UAM ConOps v2.0. Requires KPI_Common.sysml.
// Generated from article 1 and the E1 source classification. Formulas marked PROPOSED are for article 2.

package AAM_Objectives {
    doc /* AAM domain-specific Performance Objectives (article 1, Table 4). */
    private import ICAO_KPAs::*;
    private import KPI_Taxonomy::*;
    private import System_Boundaries::*;

    requirement def PO_AccessAndEquity {
        doc /* Promote equitable and practical access to AAM transportation for the intended population. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : AccessAndEquity;
    }
    requirement def PO_Capacity {
        doc /* Accommodate transportation demand within the integrated AAM operational system. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : Capacity;
    }
    requirement def PO_CostEffectiveness {
        doc /* Provide AAM transportation with efficient use of attributable system resources. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : CostEffectiveness;
    }
    requirement def PO_Efficiency {
        doc /* Improve end-to-end transportation efficiency while minimizing operational delay. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : Efficiency;
    }
    requirement def PO_Environment {
        doc /* Limit environmental burden associated with AAM transportation and operations. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : Environment;
    }
    requirement def PO_Flexibility {
        doc /* Maintain operational adaptability and continuity under changing or degraded conditions. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : Flexibility;
    }
    requirement def PO_GlobalInteroperability {
        doc /* Enable effective operational interoperability among AAM actors, systems, and infrastructure. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : GlobalInteroperability;
    }
    requirement def PO_Participation {
        doc /* Ensure meaningful engagement of relevant and affected AAM stakeholders. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : Participation;
    }
    requirement def PO_Predictability {
        doc /* Provide predictable operational outcomes with respect to planned timing. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : Predictability;
    }
    requirement def PO_Safety {
        doc /* Maintain acceptable operational safety for AAM users and affected third parties. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : Safety;
    }
    requirement def PO_Security {
        doc /* Protect AAM operations, systems, information, and stakeholders against security-related harm. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject aam : AAMSystem;
        frame concern kpa : Security;
    }
}

package AAM_KPIs {
    doc /* The 17 AAM system-level KPI candidates (article 1, Table 4). */
    private import ScalarValues::*;
    private import KPI_Taxonomy::*;
    private import KPI_Patterns::*;

    calc def <'AAM-AE-01'> PopulationServiceAccessibility {
        doc /* AAM-AE-01 -- Population Service Accessibility. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-AE-01";
            domain = Domain::AAM;
            measurementConstruct = "Geographic Accessibility";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Population within access of the service */
        attribute input1 : KPIInput {
            doc /* Population and ground-access data */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UAM §1.2.3, p. 2 (transportation equity as planning intent)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Vertiport locations and corridor definitions */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.3.1, p. 12; §4.3.7, p. 15"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-AE-02'> AffordabilityBurdenRatio {
        doc /* AAM-AE-02 -- Affordability Burden Ratio. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-AE-02";
            domain = Domain::AAM;
            measurementConstruct = "Economic Accessibility";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Fare relative to user income */
        attribute input1 : KPIInput {
            doc /* Fares and user income */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-CAP-01'> IntegratedDemandAccommodationRate :> AccommodationRate {
        doc /* AAM-CAP-01 -- Integrated Demand Accommodation Rate. Formula inherited from AccommodationRate: PROPOSED for article 2. */
        @CandidateKPI {
            code = "AAM-CAP-01";
            domain = Domain::AAM;
            measurementConstruct = "Integrated Demand Accommodation";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::ProposedInThisStudy;
        }
        comment principalQuantity /* Confirmed UAM Operational Intents */
        attribute input1 : KPIInput {
            doc /* Confirmed UAM Operational Intents */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.3.4, p. 14 (items 3-4)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Customer trip requests (denominator) */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UAM §4.3.2, p. 13; §6.1.1, p. 25"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Vertiport resource availability */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.3.7, p. 15"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input4 : KPIInput {
            doc /* Corridor availability */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.3.1, p. 12; §4.4, p. 17"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input5 : KPIInput {
            doc /* Fleet and charging availability */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "- (not addressed)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* Requests the operator cannot serve never become intents; two of the denial causes are invisible to PSUs. */
    }
    calc def <'AAM-CE-01'> CostPerCompletedOperation {
        doc /* AAM-CE-01 -- Cost per Completed AAM Operation. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-CE-01";
            domain = Domain::AAM;
            measurementConstruct = "Cost per Completed Operational Output";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Attributable system cost */
        attribute input1 : KPIInput {
            doc /* System cost */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Completed operations (mission-complete indication, archive) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §4.3.4, p. 14 (item 8); §6.1.3, p. 26"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-EFF-01'> DoorToDoorTravelTimeBenefit {
        doc /* AAM-EFF-01 -- Door-to-Door Travel-Time Benefit. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-EFF-01";
            domain = Domain::AAM;
            measurementConstruct = "Door-to-Door Travel Efficiency";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Door-to-door journey time */
        attribute input1 : KPIInput {
            doc /* Ground access and egress times */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Flight times (archived operational data) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §4.3.4, p. 14 (item 8)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Reference-mode journey time */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-EFF-02'> MeanOperationalDelay {
        doc /* AAM-EFF-02 -- Mean AAM Operational Delay. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-EFF-02";
            domain = Domain::AAM;
            measurementConstruct = "Operational Delay";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Actual minus scheduled event times */
        attribute input1 : KPIInput {
            doc /* Key event times (departure, arrival) in the confirmed intent */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §3.2, p. 8; §4.3.2, p. 13"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Actual departure (automated departure acquisition) and arrival */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §6.2.2.1, p. 27; §6.1.2, p. 25; §4.3.4, p. 14 (item 8)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-ENV-01'> LifeCycleGHGIntensity {
        doc /* AAM-ENV-01 -- Life-Cycle GHG Intensity. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-ENV-01";
            domain = Domain::AAM;
            measurementConstruct = "Climate Impact";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Life-cycle emissions per unit of output */
        attribute input1 : KPIInput {
            doc /* Energy and life-cycle emission data */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-ENV-02'> CommunityNoiseExposure {
        doc /* AAM-ENV-02 -- Community Noise Exposure. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-ENV-02";
            domain = Domain::AAM;
            measurementConstruct = "Community Noise Impact";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Noise exposure of the population */
        attribute input1 : KPIInput {
            doc /* Noise levels or acoustic model */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UAM §4.4, p. 17 (noise as a corridor design consideration only)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Flight tracks */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §6.1.2, p. 25; §4.3.4, p. 14 (item 8)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Population data */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-FLEX-01'> SuccessfulReplanningRate {
        doc /* AAM-FLEX-01 -- Successful Operational Replanning Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-FLEX-01";
            domain = Domain::AAM;
            measurementConstruct = "Operational Replanning";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Successful intent updates */
        attribute input1 : KPIInput {
            doc /* Updates to the UAM Operational Intent shared via the network */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.4.2, p. 19"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Operation outcome (mission complete) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §6.1.3, p. 26"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-FLEX-02'> DegradedOperationContinuityRate {
        doc /* AAM-FLEX-02 -- Degraded-Operation Continuity Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-FLEX-02";
            domain = Domain::AAM;
            measurementConstruct = "Operational Continuity";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Operations completed under degraded conditions */
        attribute input1 : KPIInput {
            doc /* Corridor availability and vertiport open/closed status */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.3.1, p. 12; §4.3.7, p. 15"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Off-nominal notifications */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.4.2, p. 19"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Operation outcome (mission complete) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §6.1.3, p. 26"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-GI-01'> SuccessfulInteroperabilityRate {
        doc /* AAM-GI-01 -- Successful Operational Interoperability Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-GI-01";
            domain = Domain::AAM;
            measurementConstruct = "Operational Interoperability Success";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Successful PSU-PSU, PSU-USS and FAA exchanges */
        attribute input1 : KPIInput {
            doc /* Exchange attempts and results */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UAM §2, p. 6; §5, p. 23 (common standards required, not logged)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-PART-01'> EffectiveEngagementCoverage {
        doc /* AAM-PART-01 -- Effective Stakeholder Engagement Coverage. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-PART-01";
            domain = Domain::AAM;
            measurementConstruct = "Effective Engagement Coverage";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Engaged relevant and affected stakeholders */
        attribute input1 : KPIInput {
            doc /* Engagement records */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UAM §1.2.3, p. 2; §4.2, p. 11; §4.3.10, p. 16 (process described, no data)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-PRED-01'> OperationalPunctuality :> TemporalConformanceRate {
        doc /* AAM-PRED-01 -- Operational Punctuality. Formula inherited from TemporalConformanceRate: PROPOSED for article 2. */
        @CandidateKPI {
            code = "AAM-PRED-01";
            domain = Domain::AAM;
            measurementConstruct = "Temporal Predictability";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::ProposedInThisStudy;
        }
        comment principalQuantity /* Arrivals within tolerance */
        attribute input1 : KPIInput {
            doc /* Scheduled arrival in the confirmed intent */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §3.2, p. 8"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Actual arrival (archived operational data) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §6.1.2, p. 25; §4.3.4, p. 14 (item 8)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* The ConOps names a compliance window for the arrival time but does not size it. */
    }
    calc def <'AAM-SAF-01'> SafetyOccurrenceRateBySeverity {
        doc /* AAM-SAF-01 -- Safety Occurrence Rate by Severity. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-SAF-01";
            domain = Domain::AAM;
            measurementConstruct = "Operational Safety Occurrence";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Safety occurrences */
        attribute input1 : KPIInput {
            doc /* Off-nominal event notifications */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.4.2, p. 19; §4.3.1, p. 12"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Exposure (completed operations) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §4.3.4, p. 14 (item 8)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Severity classification */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-SAF-02'> GroundThirdPartyRisk {
        doc /* AAM-SAF-02 -- Ground Third-Party Risk. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-SAF-02";
            domain = Domain::AAM;
            measurementConstruct = "Ground Third-Party Risk";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Ground risk exposure */
        attribute input1 : KPIInput {
            doc /* Population and ground exposure data, risk model */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Flight tracks */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §6.1.2, p. 25"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-SEC-01'> CybersecurityCompromiseRate {
        doc /* AAM-SEC-01 -- Cybersecurity Compromise Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-SEC-01";
            domain = Domain::AAM;
            measurementConstruct = "Cybersecurity Compromise";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Cybersecurity compromises */
        attribute input1 : KPIInput {
            doc /* Record of cyber incidents */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UAM §5, p. 23 (Service Security Gateway named, no record)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        return kpiValue : Real;
    }
    calc def <'AAM-SEC-02'> PrivacyIncidentRate {
        doc /* AAM-SEC-02 -- Privacy Incident Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "AAM-SEC-02";
            domain = Domain::AAM;
            measurementConstruct = "Privacy Compromise";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Privacy incidents */
        attribute input1 : KPIInput {
            doc /* Record of privacy incidents */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "- (privacy not addressed in the UAM ConOps)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        @DomainExtension { fit = TaxonomicFit::Provisional; }
        return kpiValue : Real;
    }
}

package AAM_Diagnostics {
    doc /* Supporting diagnostic metrics for AAM-CAP-01 (article 1, Sec. 4.5). */
    private import ScalarValues::*;
    private import KPI_Taxonomy::*;

    calc def VertiportThroughput {
        doc /* Vertiport throughput. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def PadUtilization {
        doc /* Pad utilization. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def ChargingAvailability {
        doc /* Charging availability. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def AirspaceConstraints {
        doc /* Airspace constraints. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def FleetAvailability {
        doc /* Fleet availability. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }

    dependency d_VertiportThroughput_explains from VertiportThroughput to AAM_KPIs::IntegratedDemandAccommodationRate;
    dependency d_PadUtilization_explains from PadUtilization to AAM_KPIs::IntegratedDemandAccommodationRate;
    dependency d_ChargingAvailability_explains from ChargingAvailability to AAM_KPIs::IntegratedDemandAccommodationRate;
    dependency d_AirspaceConstraints_explains from AirspaceConstraints to AAM_KPIs::IntegratedDemandAccommodationRate;
    dependency d_FleetAvailability_explains from FleetAvailability to AAM_KPIs::IntegratedDemandAccommodationRate;
}

package AAM_Traceability {
    doc /* Traceability AAM KPI -> Performance Objective (the PO frames its KPA concern). */

    dependency t_AAM_AE_01 from AAM_KPIs::PopulationServiceAccessibility to AAM_Objectives::PO_AccessAndEquity;
    dependency t_AAM_AE_02 from AAM_KPIs::AffordabilityBurdenRatio to AAM_Objectives::PO_AccessAndEquity;
    dependency t_AAM_CAP_01 from AAM_KPIs::IntegratedDemandAccommodationRate to AAM_Objectives::PO_Capacity;
    dependency t_AAM_CE_01 from AAM_KPIs::CostPerCompletedOperation to AAM_Objectives::PO_CostEffectiveness;
    dependency t_AAM_EFF_01 from AAM_KPIs::DoorToDoorTravelTimeBenefit to AAM_Objectives::PO_Efficiency;
    dependency t_AAM_EFF_02 from AAM_KPIs::MeanOperationalDelay to AAM_Objectives::PO_Efficiency;
    dependency t_AAM_ENV_01 from AAM_KPIs::LifeCycleGHGIntensity to AAM_Objectives::PO_Environment;
    dependency t_AAM_ENV_02 from AAM_KPIs::CommunityNoiseExposure to AAM_Objectives::PO_Environment;
    dependency t_AAM_FLEX_01 from AAM_KPIs::SuccessfulReplanningRate to AAM_Objectives::PO_Flexibility;
    dependency t_AAM_FLEX_02 from AAM_KPIs::DegradedOperationContinuityRate to AAM_Objectives::PO_Flexibility;
    dependency t_AAM_GI_01 from AAM_KPIs::SuccessfulInteroperabilityRate to AAM_Objectives::PO_GlobalInteroperability;
    dependency t_AAM_PART_01 from AAM_KPIs::EffectiveEngagementCoverage to AAM_Objectives::PO_Participation;
    dependency t_AAM_PRED_01 from AAM_KPIs::OperationalPunctuality to AAM_Objectives::PO_Predictability;
    dependency t_AAM_SAF_01 from AAM_KPIs::SafetyOccurrenceRateBySeverity to AAM_Objectives::PO_Safety;
    dependency t_AAM_SAF_02 from AAM_KPIs::GroundThirdPartyRisk to AAM_Objectives::PO_Safety;
    dependency t_AAM_SEC_01 from AAM_KPIs::CybersecurityCompromiseRate to AAM_Objectives::PO_Security;
    dependency t_AAM_SEC_02 from AAM_KPIs::PrivacyIncidentRate to AAM_Objectives::PO_Security;
}
